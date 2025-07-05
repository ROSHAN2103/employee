from django.shortcuts import render

import io
import requests
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render
import matplotlib.pyplot as plt

API_URL = (
    "https://rc-vault-fap-live-1.azurewebsites.net/api/gettimeentries?code=vO17RnE8vuzXzPJo5eaLLjXjmRW07law99QTD90zat9FfOQJKKUcgQ=="
)

def _get_totals():
    """Return list of (name, total_hours) tuples, sorted desc."""
    resp = requests.get(API_URL, timeout=20)
    resp.raise_for_status()
    data = resp.json()          
    totals = defaultdict(float)
    for row in data:
        totals[row["employeeName"]] += row["timeWorked"]
        return sorted(
        [{"name": k, "hours": v} for k, v in totals.items()],
        key=lambda x: x["hours"],
        reverse=True,
    )

def employee_table(request):
    totals = _get_totals()
    return render(request, "dashboard/templates/table.html", {"employees": totals})

def pie_png(request):
    totals = _get_totals()
    labels = [e["name"] for e in totals]
    hours  = [e["hours"] for e in totals]

    fig, ax = plt.subplots()
    ax.pie(hours, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Share of Total Hours Worked")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type="image/png")

