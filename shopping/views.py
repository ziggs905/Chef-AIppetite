from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from mealplans.models import WeeklyPlan

from .forms import ShoppingItemForm
from .models import ShoppingList
from .services import generate_shopping_list


@login_required
def shopping_list_index(request):
    shopping_lists = ShoppingList.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'shopping/shopping_list_index.html', {'shopping_lists': shopping_lists})


@login_required
@require_POST
def shopping_list_generate(request, plan_pk):
    plan = get_object_or_404(WeeklyPlan, pk=plan_pk, owner=request.user)
    shopping_list = generate_shopping_list(request.user, plan, f'Shopping list for {plan.name}')
    return redirect('shopping_list_detail', pk=shopping_list.pk)


@login_required
def shopping_list_detail(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    items = shopping_list.items.all()
    if request.method == 'POST':
        form = ShoppingItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.shopping_list = shopping_list
            item.position = items.count()
            item.save()
            return redirect('shopping_list_detail', pk=shopping_list.pk)
    else:
        form = ShoppingItemForm()
    return render(request, 'shopping/shopping_list_detail.html', {
        'shopping_list': shopping_list, 'items': items, 'form': form,
    })


@login_required
def shopping_list_delete(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    if request.method == 'POST':
        shopping_list.delete()
        return redirect('shopping_list_index')
    return render(request, 'shopping/shopping_list_confirm_delete.html', {'shopping_list': shopping_list})


@login_required
def shopping_item_edit(request, pk, item_pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    item = get_object_or_404(shopping_list.items, pk=item_pk)
    if request.method == 'POST':
        form = ShoppingItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('shopping_list_detail', pk=shopping_list.pk)
    else:
        form = ShoppingItemForm(instance=item)
    return render(request, 'shopping/shopping_item_form.html', {
        'shopping_list': shopping_list, 'form': form,
    })


@login_required
def shopping_item_delete(request, pk, item_pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    item = get_object_or_404(shopping_list.items, pk=item_pk)
    if request.method == 'POST':
        item.delete()
    return redirect('shopping_list_detail', pk=shopping_list.pk)


@login_required
@require_POST
def shopping_item_toggle(request, pk, item_pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk, owner=request.user)
    item = get_object_or_404(shopping_list.items, pk=item_pk)
    item.checked = not item.checked
    item.save(update_fields=['checked'])
    return JsonResponse({'checked': item.checked})
