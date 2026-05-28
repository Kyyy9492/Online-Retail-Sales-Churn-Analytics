import matplotlib.pyplot as plt


def plot_monthly_revenue(monthly_sales):
    plt.figure(figsize=(12, 5))
    plt.plot(monthly_sales["invoice_month"], monthly_sales["total_revenue"])
    plt.xticks(rotation=75)
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Invoice Month")
    plt.ylabel("Revenue")
    plt.tight_layout()
    return plt.gcf()


def plot_segment_revenue(segment_summary):
    data = segment_summary.sort_values("revenue")
    plt.figure(figsize=(10, 5))
    plt.barh(data["customer_segment"], data["revenue"])
    plt.title("Revenue by Customer Segment")
    plt.xlabel("Revenue")
    plt.tight_layout()
    return plt.gcf()
