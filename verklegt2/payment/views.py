from django.shortcuts import render, get_object_or_404, redirect
from property.models import PurchaseOffer
from .forms import (
    ContactInfoForm,
    PaymentMethodForm,
    CreditCardForm,
    BankTransferForm,
    MortgageForm,
)


def finalize_offer(request, offer_id, step):
    offer = get_object_or_404(PurchaseOffer, id=offer_id)

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

    elif step == "payment":
        form = PaymentMethodForm(request.POST or None)
        selected_payment_method = None

        if request.method == "POST" and form.is_valid():
            selected_payment_method = form.cleaned_data["payment_method"]
            request.session["payment_method"] = selected_payment_method
            return redirect(
                "finalize_offer", offer_id=offer.id, step=selected_payment_method
            )

        selected_payment_method = request.POST.get(
            "payment_method"
        ) or request.session.get("payment_method")

        return render(
            request,
            "payment/payment.html",
            {
                "form": form,
                "offer": offer,
                "step": step,
                "step_number": 2,
                "selected_payment_method": selected_payment_method,
            },
        )

    elif step == "credit_card":
        form = CreditCardForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            request.session["payment_data"] = form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="review")

        return render(
            request,
            "payment/payment.html",
            {
                "form": form,
                "offer": offer,
                "step": step,
                "step_number": 3,
                "selected_payment_method": "credit_card",
            },
        )

    elif step == "bank_transfer":
        form = BankTransferForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            request.session["payment_data"] = form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="review")

        return render(
            request,
            "payment/payment.html",
            {
                "form": form,
                "offer": offer,
                "step": step,
                "step_number": 3,
                "selected_payment_method": "bank_transfer",
            },
        )

    elif step == "mortgage":
        form = MortgageForm(request.POST or None)

        if request.method == "POST" and form.is_valid():
            request.session["payment_data"] = form.cleaned_data
            return redirect("finalize_offer", offer_id=offer.id, step="review")

        return render(
            request,
            "payment/payment.html",
            {
                "form": form,
                "offer": offer,
                "step": step,
                "step_number": 3,
                "selected_payment_method": "mortgage",
            },
        )

    elif step == "review":
        if request.method == "POST":
            # Finalize the offer on form submission
            offer.status = "finalized"
            offer.save()
            return redirect("finalize_offer", offer_id=offer.id, step="confirmation")

        # For GET: display review info
        contact_data = request.session.get("contact_data", {})
        payment_data = request.session.get("payment_data", {})
        payment_method = request.session.get("payment_method", None)

        finalization = {
            **contact_data,
            **payment_data,
            "payment_method": payment_method,
        }

        property_obj = offer.property
        owner = getattr(property_obj, "owner", None)

        return render(
            request,
            "payment/review.html",
            {
                "finalization": finalization,
                "offer": offer,
                "property": property_obj,
                "owner": owner,
                "step": step,
                "step_number": 4,
            },
        )

    elif step == "confirmation":
        # Mark offer as finalized
        offer.status = "finalized"
        offer.save()

        request.session.flush()

        return render(
            request,
            "payment/confirmation.html",
            {
                "offer": offer,
                "step": step,
                "step_number": 5,
            },
        )

    return redirect("finalize_offer", offer_id=offer.id, step="contact")
