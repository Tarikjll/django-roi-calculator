from decimal import Decimal, InvalidOperation

from django.shortcuts import render

from .models import ROICalculation


def index(request):
    result = None
    error = None

    if request.method == "POST":
        try:
            investment_cost = Decimal(request.POST.get("investment_cost", "0"))
            revenue = Decimal(request.POST.get("revenue", "0"))
            operating_costs = Decimal(request.POST.get("operating_costs", "0"))

            if investment_cost <= 0:
                error = "De investeringskost moet groter zijn dan 0."
            elif revenue < 0 or operating_costs < 0:
                error = "Opbrengst en operationele kosten mogen niet negatief zijn."
            else:
                total_costs = investment_cost + operating_costs
                net_result = revenue - total_costs
                roi_percentage = (net_result / investment_cost) * 100

                if revenue > 0:
                    profit_margin = (net_result / revenue) * 100
                else:
                    profit_margin = Decimal("0")

                if net_result > 0:
                    break_even_status = "De investering is winstgevend."
                elif net_result == 0:
                    break_even_status = "De investering staat exact break-even."
                else:
                    break_even_status = "De investering maakt verlies."

                if roi_percentage >= 20:
                    evaluation = "Sterke investering"
                elif roi_percentage >= 5:
                    evaluation = "Aanvaardbare investering"
                elif roi_percentage >= 0:
                    evaluation = "Lage maar positieve investering"
                else:
                    evaluation = "Risicovolle investering"

                calculation = ROICalculation.objects.create(
                    investment_cost=investment_cost,
                    revenue=revenue,
                    operating_costs=operating_costs,
                    net_result=net_result,
                    roi_percentage=roi_percentage,
                    profit_margin=profit_margin,
                    evaluation=evaluation,
                )

                result = {
                    "investment_cost": round(calculation.investment_cost, 2),
                    "revenue": round(calculation.revenue, 2),
                    "operating_costs": round(calculation.operating_costs, 2),
                    "total_costs": round(total_costs, 2),
                    "net_result": round(calculation.net_result, 2),
                    "roi_percentage": round(calculation.roi_percentage, 2),
                    "profit_margin": round(calculation.profit_margin, 2),
                    "break_even_status": break_even_status,
                    "evaluation": calculation.evaluation,
                }

        except InvalidOperation:
            error = "Gelieve geldige numerieke waarden in te geven."

    recent_calculations = ROICalculation.objects.order_by("-created_at")[:5]

    return render(request, "scientific_app/index.html", {
        "result": result,
        "error": error,
        "recent_calculations": recent_calculations,
    })