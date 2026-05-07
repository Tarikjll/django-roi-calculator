from django.db import models


class ROICalculation(models.Model):
    investment_cost = models.DecimalField(max_digits=10, decimal_places=2)
    revenue = models.DecimalField(max_digits=10, decimal_places=2)
    operating_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    net_result = models.DecimalField(max_digits=10, decimal_places=2)
    roi_percentage = models.DecimalField(max_digits=7, decimal_places=2)
    profit_margin = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    evaluation = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ROI calculation - {self.created_at}"