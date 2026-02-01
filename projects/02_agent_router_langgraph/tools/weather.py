from pydantic import BaseModel, Field


class WeatherInput(BaseModel):
    city: str = Field(..., description="City to fetch weather for")


def run_weather(input_data: WeatherInput) -> str:
    return f"Sunny in {input_data.city}."  # TODO: replace with real API
