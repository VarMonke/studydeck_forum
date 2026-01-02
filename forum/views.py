from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import Reply, Thread


@login_required
@require_POST
def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)

    if request.user == reply.author or request.user.has_perm("forum.delete_any_reply"):
        reply.is_deleted = True
        reply.save()
        return redirect(request.META.get("HTTP_REFERER", "/"))

    raise PermissionDenied


@login_required
@require_POST
def ban_user(request, user_id):
    if not request.user.has_perm("auth.change_user"):
        raise PermissionDenied

    target = get_object_or_404(User, id=user_id)
    target.is_active = False
    target.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
@require_POST
def lock_thread(request, thread_id):
    if not request.user.has_perm("forum.lock_thread"):
        raise PermissionDenied

    thread = get_object_or_404(Thread, id=thread_id)
    thread.is_locked = True
    thread.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))
