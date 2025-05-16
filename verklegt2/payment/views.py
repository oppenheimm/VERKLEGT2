from django.shortcuts import render, get_object_or_404, redirect
from property.models import PurchaseOffer
from .forms import (
    ContactInfoForm,
    PaymentMethodForm,
    CreditCardForm,
    BankTransferForm,
    MortgageForm,
)


def _handle_method_switch(request, offer_id):
    """If the selector was the only thing posted, just redirect to the new step."""
    if "payment_method" not in request.POST:
        return None

    method_form = PaymentMethodForm(request.POST)
    if method_form.is_valid():
        new_method = method_form.cleaned_data["payment_method"]
        request.session["payment_method"] = new_method
        return redirect("finalize_offer", offer_id=offer_id, step=new_method)
    return None


def finalize_offer(request, offer_id, step):
    """Multi-step purchase flow: contact → payment → details → review → confirmation."""
    offer = get_object_or_404(PurchaseOffer, id=offer_id)

    # ───────────── STEP 1: contact info ─────────────
    if step == "contact":
        form = ContactInfoForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            request.session["contact_data"] = form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="payment")

        return render(
            request,
            "payment/contact.html",
            {
                "form": form,
                "offer": offer,
                "step": step,
                "step_number": 1,
            },
        )

    # ───────────── STEP 2: choose payment method ─────────────
    elif step == "payment":
        method_form = PaymentMethodForm(request.POST or None)
        if request.method == "POST" and method_form.is_valid():
            selected = method_form.cleaned_data["payment_method"]
            request.session["payment_method"] = selected
            return redirect("finalize_offer", offer_id=offer.id, step=selected)

        selected = request.session.get("payment_method")
        return render(request, "payment/payment.html", {
            "form": method_form,          # backward-compat
            "method_form": method_form,   # always the selector
            "offer": offer,
            "step": step,
            "step_number": 2,
            "selected_payment_method": selected,
        })

    # handle quick selector switches on detail steps
    redirect_if_switch = _handle_method_switch(request, offer_id)
    if redirect_if_switch:
        return redirect_if_switch

    # ───────────── STEP 3a: credit-card details ─────────────
    if step == "credit_card":
        data_form = CreditCardForm(request.POST or None)
        method_form = PaymentMethodForm(initial={"payment_method": "credit_card"})

        if request.method == "POST" and "payment_method" not in request.POST and data_form.is_valid():
            request.session["payment_data"] = data_form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="review")

        return render(request, "payment/payment.html", {
            "form": data_form,
            "method_form": method_form,
            "offer": offer,
            "step": step,
            "step_number": 3,
            "selected_payment_method": "credit_card",
        })

    # ───────────── STEP 3b: bank-transfer details ─────────────
    if step == "bank_transfer":
        data_form = BankTransferForm(request.POST or None)
        method_form = PaymentMethodForm(initial={"payment_method": "bank_transfer"})

        if request.method == "POST" and "payment_method" not in request.POST and data_form.is_valid():
            request.session["payment_data"] = data_form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="review")

        return render(request, "payment/payment.html", {
            "form": data_form,
            "method_form": method_form,
            "offer": offer,
            "step": step,
            "step_number": 3,
            "selected_payment_method": "bank_transfer",
        })

    # ───────────── STEP 3c: mortgage details ─────────────
    if step == "mortgage":
        data_form = MortgageForm(request.POST or None)
        method_form = PaymentMethodForm(initial={"payment_method": "mortgage"})

        if request.method == "POST" and "payment_method" not in request.POST and data_form.is_valid():
            request.session["payment_data"] = data_form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="review")

        return render(request, "payment/payment.html", {
            "form": data_form,
            "method_form": method_form,
            "offer": offer,
            "step": step,
            "step_number": 3,
            "selected_payment_method": "mortgage",
        })

    # ───────────── STEP 4: review ─────────────
    elif step == "review":
        if request.method == "POST":
            offer.status = "finalized"
            offer.save()
            return redirect("finalize_offer", offer_id=offer.id, step="confirmation")

        contact_data  = request.session.get("contact_data", {})
        payment_data  = request.session.get("payment_data", {})
        payment_method = request.session.get("payment_method")

        # ▲ include payment_data so card / bank / mortgage fields appear
        finalization = {
            **contact_data,
            **payment_data,
            "payment_method": payment_method,
        }

        prop  = offer.property
        owner = getattr(prop, "owner", None)

        return render(request, "payment/review.html", {
            "finalization": finalization,
            "offer": offer,
            "property": prop,
            "owner": owner,
            "step": step,
            "step_number": 4,
        })

    # ───────────── STEP 5: confirmation ─────────────
    elif step == "confirmation":
        offer.status = "finalized"
        offer.save()
        request.session.flush()
        return render(request, "payment/confirmation.html", {
            "offer": offer,
            "step": step,
            "step_number": 5,
        })

    # fallback → restart flow
    return redirect("finalize_offer", offer_id=offer.id, step="contact")
