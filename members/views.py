from django.shortcuts import render, redirect, get_object_or_404
from geopy.distance import geodesic
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser


from .forms import UserRegistrationForm, ClientEditForm
from .models import Client
from .filters import ClientFilter
from .serializers import MembersSerializer

UserModel = get_user_model()


def register(request):

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Client.objects.create(user=new_user)
            current_site = get_current_site(request)
            mail_subject = 'Активация Вашего аккаунта'
            message = render_to_string('notifications/acc_active_email.html', {
                'new_user': new_user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': default_token_generator.make_token(new_user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return render(request, 'members/confirm_register_email.html', locals())
    else:
        user_form = UserRegistrationForm()

    return render(request, 'members/registration.html', locals())


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        client = Client.objects.get(user=user)
        client.is_active = True
        client.save()
        return render(request, 'members/register_done.html', locals())
    else:
        return render(request, 'members/register_failed.html', locals())


@login_required
def edit_account(request):
    if request.method == 'POST':
        client_form = ClientEditForm(instance=request.user.client, data=request.POST, files=request.FILES)
        if client_form.is_valid():
            client_edited = client_form.save(commit=False)
            client_edited.user = request.user
            client_edited.save()
            # client_form.save()
            return redirect('clients:list')
        else:
            messages.error(request, 'Ваш профиль не был изменен, пожалуйста, проверьте введенные Вами данные')
    else:
        client_form = ClientEditForm()

    return render(request, 'members/edit_account.html', locals())


def match(request, id):
    current_user = request.user
    favorite = get_object_or_404(Client, id=id, is_active=True)
    mail_subject_for_favorite = 'Вы понравились кому-то!'
    message_for_favorite = render_to_string('notifications/match_favorite_email.html', locals())
    to_favorite_email = favorite.user.email
    email_to_favorite = EmailMessage(mail_subject_for_favorite, message_for_favorite, to=[to_favorite_email])
    email_to_favorite.send()
    mail_subject_for_user = 'Вы поставили лайк!'
    message_for_user = render_to_string('notifications/match_current_user_email.html', locals())
    to_user_email = current_user.email
    email_to_user = EmailMessage(mail_subject_for_user, message_for_user, to=[to_user_email])
    email_to_user.send()
    return render(request, 'members/favorite_client.html', locals())


def clients_list(request):

    current_user = request.user
    clients = Client.objects.filter(is_active=True)

    if request.method == 'GET':
        for member in clients:
            a = (current_user.client.longitude, current_user.client.latitude)
            b = (member.longitude, member.latitude)
            distance = [round(geodesic(a, b).kilometers, 2)]
            print(distance)
            clients = ClientFilter(request.GET, queryset=Client.objects.filter(is_active=True))
    return render(request, 'members/list.html', locals())


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'


class MemberList(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_active=True)
    serializer_class = MembersSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['gender']
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    search_fields = ['last_name', 'first_name']
    lookup_field = 'pk'
