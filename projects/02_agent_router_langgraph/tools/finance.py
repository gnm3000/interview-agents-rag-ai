from pydantic import BaseModel, Field


class FinanceInput(BaseModel):
    ticker: str = Field(..., description="Ticker symbol")


def run_finance(input_data: FinanceInput) -> str:
    return f"{input_data.ticker} closed at $123.45."  # TODO: real market data
