from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Reply, Thread,  Resource, Vote, Report
from .forms import ReplyForm, ThreadForm


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

@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    replies = Reply.objects.filter(thread=thread).order_by("created_at")

    paginator = Paginator(replies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # ---- VOTE STATE ----
    thread_vote = 0
    reply_votes = {}

    if request.user.is_authenticated:
        thread_vote_obj = Vote.objects.filter(
            user=request.user, thread=thread
        ).first()
        if thread_vote_obj:
            thread_vote = thread_vote_obj.value

        reply_vote_qs = Vote.objects.filter(
            user=request.user, reply__in=page_obj
        )
        reply_votes = {v.reply_id: v.value for v in reply_vote_qs} #type: ignore

        for reply in page_obj:
            reply.vote_value = reply_votes.get(reply.id, 0)

    return render(
        request,
        "forum/thread_detail.html",
        {
            "thread": thread,
            "page_obj": page_obj,
            "thread_vote": thread_vote,
            "reply_votes": reply_votes,
        },
    )


@login_required
def thread_list(request):
    threads = Thread.objects.all()

    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")

    if category_slug:
        threads = threads.filter(category__slug=category_slug.lower())

    if tag_slug:
        threads = threads.filter(tags__slug=tag_slug.lower())

    threads = threads.order_by("-created_at")

    paginator = Paginator(threads, 15)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "forum/thread_list.html",
        {
            "page_obj": page_obj,
            "selected_category": category_slug,
            "selected_tag": tag_slug,
        },
    )



@login_required
def add_reply(request, thread_id):
    thread = get_object_or_404(Thread, id=thread_id)

    if thread.is_locked:
        raise PermissionDenied("Thread is locked")

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.thread = thread
            reply.save()

            # 🔑 Compute last page
            replies_qs = Reply.objects.filter(thread=thread).order_by("created_at")
            paginator = Paginator(replies_qs, 10)  # SAME page size as thread_detail
            last_page = paginator.num_pages

            return redirect(f"/threads/{thread.id}/?page={last_page}") #type: ignore

    return redirect("thread_detail", thread_id=thread.id) #type: ignore


@login_required
def create_thread(request):
    if request.method == "POST":
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.author = request.user
            thread.save()
            form.save_m2m()  # save tags

            # ---- HANDLE RESOURCE ----
            resource_url = request.POST.get("resource_url")
            resource_title = request.POST.get("resource_title")

            if resource_url:
                resource = Resource.objects.create(
                    title=resource_title or "Shared Resource",
                    url=resource_url,
                    created_by=request.user,
                )
                thread.resources.add(resource)

            return redirect("thread_detail", thread_id=thread.id)
    else:
        form = ThreadForm()

    return render(
        request,
        "forum/create_thread.html",
        {"form": form}
    )



@login_required
def vote(request, kind, obj_id, direction):
    if direction == "up":
        value = 1
    elif direction == "down":
        value = -1
    else:
        raise PermissionDenied

    if kind == "thread":
        obj = get_object_or_404(Thread, id=obj_id)

        # 🚫 Block voting on locked threads
        if obj.is_locked:
            raise PermissionDenied("Thread is locked")

        vote_filter = {"user": request.user, "thread": obj, "reply": None}

    elif kind == "reply":
        obj = get_object_or_404(Reply, id=obj_id)

        # 🚫 Block voting on deleted replies
        if obj.is_deleted:
            raise PermissionDenied("Cannot vote on deleted reply")

        # 🚫 Block voting if thread is locked
        if obj.thread.is_locked:
            raise PermissionDenied("Thread is locked")

        vote_filter = {"user": request.user, "reply": obj, "thread": None}
    else:
        raise PermissionDenied

    existing = Vote.objects.filter(**vote_filter).first()

    if existing:
        if existing.value == value:
            existing.delete()
        else:
            existing.value = value
            existing.save()
    else:
        Vote.objects.create(**vote_filter, value=value)

    if kind == "thread":
        return redirect("thread_detail", thread_id=obj.id) #type: ignore
    else:
        return redirect("thread_detail", thread_id=obj.thread.id) #type: ignore


@login_required
def report(request):
    if request.method != "POST":
        raise PermissionDenied

    Report.objects.create(
        reporter=request.user,
        target_type=request.POST["target_type"],
        target_id=request.POST["target_id"],
        reason=request.POST.get("reason", "No reason provided"),
    )

    return redirect(request.META.get("HTTP_REFERER", "/"))


@permission_required("forum.delete_any_reply")
def report_queue(request):
    pending_reports = Report.objects.filter(
        status="pending"
    ).order_by("-created_at")

    resolved_reports = Report.objects.filter(
        status="resolved"
    ).order_by("-created_at")

    return render(
        request,
        "forum/report_queue.html",
        {
            "pending_reports": pending_reports,
            "resolved_reports": resolved_reports,
        }
    )



@permission_required("forum.delete_any_reply")
def resolve_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.status = "resolved"
    report.save()
    return redirect("report_queue")


@login_required
def report_form(request, target_type, target_id):
    if target_type not in ["thread", "reply", "resource"]:
        raise PermissionDenied

    if request.method == "POST":
        Report.objects.create(
            reporter=request.user,
            target_type=target_type,
            target_id=target_id,
            reason=request.POST["reason"],
        )
        return redirect("/threads/")

    return render(
        request,
        "forum/report_form.html",
        {
            "target_type": target_type,
            "target_id": target_id,
        }
    )
