import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set page title
st.title("Sensitivity Analysis: NPV & Payback Period")

# Move sliders to the top for better mobile usability
st.subheader("Adjust Variables")
electricity_price = st.slider("Electricity Price (€/kWh)", 0.05, 0.3, 0.1, 0.01)
gas_price = st.slider("Gas Price (€/kWh)", 0.02, 0.1, 0.05, 0.005)

# Investment options data
investments = [
    {"name": "Investment 1", "cost": 180000, "gas_savings_base": 139727, "electricity_consumption": 282948, "maintenance": 4500, "pv_factor": 8.443793688},
    {"name": "Investment 2", "cost": 240000, "gas_savings_base": 169864, "electricity_consumption": 443840, "maintenance": 6000, "pv_factor": 8.443793688},
    {"name": "Investment 3", "cost": 350000, "gas_savings_base": 221666, "electricity_consumption": 598500, "maintenance": 8750, "pv_factor": 8.443793688},
]

def calculate_net_savings(gas_savings_base, electricity_consumption, maintenance, gas_price, electricity_price):
    gas_savings = gas_savings_base * gas_price  # Gas savings change with gas price
    electricity_cost = electricity_consumption * electricity_price  # Electricity cost depends on price
    net_savings = gas_savings - electricity_cost - maintenance
    return max(net_savings, 0)  # Ensure savings do not go negative

def calculate_payback(investment_cost, net_savings):
    if net_savings <= 0:
        return float("inf")  # If no savings, payback is impossible
    return investment_cost / net_savings

def calculate_npv(net_savings, pv_factor):
    return max(net_savings * pv_factor, 0)  # Ensure NPV does not go negative

# Generate dynamic values
npv_values = []
payback_values = []
investment_names = []

for investment in investments:
    net_savings = calculate_net_savings(investment["gas_savings_base"], investment["electricity_consumption"], investment["maintenance"], gas_price, electricity_price)
    updated_npv = calculate_npv(net_savings, investment["pv_factor"])
    updated_payback = calculate_payback(investment["cost"], net_savings)
    npv_values.append(updated_npv)
    payback_values.append(updated_payback)
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
