import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title
st.title("Sensitivity Analysis: NPV & Payback Period")

# Sidebar inputs
st.sidebar.header("Adjust Variables")
electricity_price = st.sidebar.slider("Electricity Price (€/kWh)", 0.05, 0.3, 0.1, 0.01)
gas_price = st.sidebar.slider("Gas Price (€/kWh)", 0.02, 0.1, 0.05, 0.005)

# Constants
initial_investment = 100000
annual_savings_base = 20000
discount_rate = 0.05
years = 10

# Functions to calculate NPV & Payback Period
def calculate_npv(electricity, gas):
    npv = 0
    annual_savings = annual_savings_base + (electricity * 5000) - (gas * 3000)
    for t in range(1, years + 1):
        npv += annual_savings / (1 + discount_rate) ** t
    return npv - initial_investment

def calculate_payback(electricity, gas):
    annual_savings = annual_savings_base + (electricity * 5000) - (gas * 3000)
    return initial_investment / annual_savings

# Calculate values
npv = calculate_npv(electricity_price, gas_price)
payback = calculate_payback(electricity_price, gas_price)

# Display results
st.metric("Net Present Value (NPV)", f"€ {npv:,.2f}")
st.metric("Payback Period", f"{payback:.2f} years")

# Generate data for sensitivity analysis
electricity_values = np.linspace(0.05, 0.3, 20)
npv_values = [calculate_npv(e, gas_price) for e in electricity_values]
payback_values = [calculate_payback(e, gas_price) for e in electricity_values]

# Plot results
fig, ax = plt.subplots()
ax.plot(electricity_values, npv_values, label="NPV (€)", color='blue')
ax.plot(electricity_values, payback_values, label="Payback Period (years)", color='red')
ax.set_xlabel("Electricity Price (€/kWh)")
ax.set_ylabel("Values")
ax.legend()
ax.grid(True)

# Display chart
st.pyplot(fig)
