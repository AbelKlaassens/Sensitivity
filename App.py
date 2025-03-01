import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page title
st.title("Sensitivity Analysis: NPV & Payback Period")

# Move sliders to the top for better mobile usability
st.subheader("Adjust Variables")
electricity_price = st.slider("Electricity Price (€/kWh)", 0.05, 0.3, 0.1, 0.01)
gas_price = st.slider("Gas Price (€/kWh)", 0.02, 0.1, 0.053, 0.005)

# Constants
lower_heating_value = 9.5  # kWh/m3

# Investment options data directly from the table
investments = [
    {"name": "Investment 1", "cost": 180000, "gas_savings_m3": 139727.4074, "co2_savings": 26548.20741, "electricity_consumption": 282948, "maintenance": 4500, "pv_factor": 8.443793688},
    {"name": "Investment 2", "cost": 240000, "gas_savings_m3": 169864.6914, "co2_savings": 32274.29136, "electricity_consumption": 443840, "maintenance": 6000, "pv_factor": 8.443793688},
    {"name": "Investment 3", "cost": 350000, "gas_savings_m3": 221666.6667, "co2_savings": 42116.66667, "electricity_consumption": 598500, "maintenance": 8750, "pv_factor": 8.443793688},
]

# Function to calculate Gas Savings (€)
def calculate_gas_savings(gas_savings_m3, gas_price, lower_heating_value):
    return gas_savings_m3 * gas_price * lower_heating_value

# Function to calculate Electricity Cost (€)
def calculate_electricity_cost(electricity_consumption, electricity_price):
    return electricity_consumption * electricity_price

# Function to calculate Net Financial Savings (€)
def calculate_net_savings(gas_savings, co2_savings, electricity_cost, maintenance):
    return gas_savings + co2_savings - electricity_cost - maintenance

# Function to calculate Payback Period
def calculate_payback(investment_cost, net_savings):
    return investment_cost / net_savings if net_savings > 0 else float("inf")

# Function to calculate NPV
def calculate_npv(net_savings, pv_factor):
    return net_savings * pv_factor if net_savings > 0 else 0

# Generate dynamic values
npv_values = []
payback_values = []
investment_names = []

for investment in investments:
    gas_savings = calculate_gas_savings(investment["gas_savings_m3"], gas_price, lower_heating_value)
    electricity_cost = calculate_electricity_cost(investment["electricity_consumption"], electricity_price)
    net_savings = calculate_net_savings(gas_savings, investment["co2_savings"], electricity_cost, investment["maintenance"])
    updated_npv = calculate_npv(net_savings, investment["pv_factor"])
    updated_payback = calculate_payback(investment["cost"], net_savings)
    npv_values.append(updated_npv)
    payback_values.append(updated_payback if updated_payback < float("inf") else 0)  # Avoid infinite values
    investment_names.append(investment["name"])

# Plot NPV Graph
fig_npv, ax_npv = plt.subplots()
ax_npv.bar(investment_names, npv_values, color=['blue', 'green', 'red'])
ax_npv.set_ylabel("Net Present Value (€)")
ax_npv.set_title("NPV for Each Investment Option")
ax_npv.grid(True)

# Plot Payback Period Graph
fig_payback, ax_payback = plt.subplots()
ax_payback.bar(investment_names, payback_values, color=['purple', 'orange', 'cyan'])
ax_payback.set_ylabel("Payback Period (Years)")
ax_payback.set_title("Payback Period for Each Investment Option")
ax_payback.grid(True)

# Display Graphs in Streamlit
st.subheader("Results")
st.pyplot(fig_npv)
st.pyplot(fig_payback)