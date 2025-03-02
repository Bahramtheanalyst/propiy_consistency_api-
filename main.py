from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# مدل ورودی برای محاسبه امتیاز ثبات
class ScoreInput(BaseModel):
    daily_profits: List[float]  # لیست سود و زیان‌های روزانه

@app.get("/")
def home():
    return {"message": "API for Consistency Score is running!"}

@app.get("/info")
def get_info():
    return {
        "title": "امتیاز ثبات معامله‌گری",
        "description": "امتیاز ثبات نشان‌دهنده‌ی میزان پایداری معاملات شماست. اگر سود و زیان شما به‌طور متعادل توزیع شده باشد، امتیاز بالاتری خواهید داشت.",
        "formula": "Consistency Score = (1 - (Max Absolute Daily Profit or Loss / Total Absolute Profit and Loss)) * 100",
        "importance": "این امتیاز به شما کمک می‌کند تا استراتژی معاملاتی باثبات‌تری داشته باشید و از نوسانات شدید جلوگیری کنید."
    }

@app.post("/calculate")
def calculate_score(data: ScoreInput):
    if not data.daily_profits:
        return {"error": "لطفاً لیست سود و زیان‌های روزانه را وارد کنید."}
    
    absolute_profits = [abs(p) for p in data.daily_profits]
    max_profit = max(absolute_profits)
    total_profit = sum(absolute_profits)

    if total_profit == 0:
        return {"score": 0, "message": "امتیاز نمی‌تواند محاسبه شود زیرا مجموع سود و زیان صفر است."}

    score = (1 - (max_profit / total_profit)) * 100
    return {"consistency_score": round(score, 2)}

@app.get("/improvement-tips")
def get_tips():
    return {
        "tips": [
            "از انجام معاملات با حجم بسیار بالا خودداری کنید تا از سود یا زیان ناگهانی جلوگیری شود.",
            "عملکرد خود را در بازه‌های زمانی متعادل نگه دارید و از نوسانات شدید دوری کنید.",
            "مدیریت سرمایه صحیح را رعایت کنید تا سود و زیان روزانه در یک محدوده معقول باقی بماند."
        ]
    }
