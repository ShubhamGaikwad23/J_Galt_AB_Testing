# ========================================
# Step 1: Import Required Libraries
# ========================================
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ========================================
# Step 2: Simulate Sample A/B Test Data
# ========================================
np.random.seed(42)
n_A = 1000  # Control group
n_B = 1000  # Variant group

clicks_A = np.random.binomial(1, 0.10, n_A)   # 10% CTR
clicks_B = np.random.binomial(1, 0.125, n_B)  # 12.5% CTR

data = pd.DataFrame({
    "user_id": range(1, n_A + n_B + 1),
    "group": ['A'] * n_A + ['B'] * n_B,
    "clicked": np.concatenate([clicks_A, clicks_B])
})

# ========================================
# Step 3: Group-Wise Summary Stats
# ========================================
summary = data.groupby("group")['clicked'].agg(['count', 'sum'])
summary['CTR (%)'] = (summary['sum'] / summary['count']) * 100
print("=== Summary Statistics ===")
print(summary)

# ========================================
# Step 4: Z-Test for Proportions
# ========================================
count = np.array([summary.loc['A', 'sum'], summary.loc['B', 'sum']])
nobs = np.array([summary.loc['A', 'count'], summary.loc['B', 'count']])
z_stat, p_val = proportions_ztest(count, nobs)

print("\n=== Z-Test Results ===")
print(f"Z-Statistic: {z_stat:.4f}")
print(f"P-Value: {p_val:.4f}")
significant = p_val < 0.05
print("Significant at 0.05 level?", "Yes ✅" if significant else "No ❌")

# ========================================
# Step 5: Visualize CTR Comparison
# ========================================
plt.figure(figsize=(6, 4))
sns.barplot(x=summary.index, y=summary["CTR (%)"], palette=["steelblue", "seagreen"])
plt.title("Click-Through Rate (CTR) by Group")
plt.ylabel("CTR (%)")
plt.xlabel("Group")
plt.ylim(0, max(summary["CTR (%)"]) + 5)
for i, val in enumerate(summary["CTR (%)"]):
    plt.text(i, val + 0.5, f"{val:.1f}%", ha='center')
plt.tight_layout()
plt.show()

# ========================================
# Step 6: Final Business Conclusion
# ========================================
print("\n=== Final Business Conclusion ===")
if significant:
    print(
        f"✅ The A/B test shows a statistically significant improvement in CTR from {summary.loc['A', 'CTR (%)']:.1f}% to "
        f"{summary.loc['B', 'CTR (%)']:.1f}%. Variant B should be rolled out for future campaigns to boost engagement."
    )
else:
    print(
        f"⚠️ Although Variant B had a higher CTR ({summary.loc['B', 'CTR (%)']:.1f}%) than Control A ({summary.loc['A', 'CTR (%)']:.1f}%), "
        "the difference is not statistically significant. We recommend gathering more data or testing additional variations."
    )
