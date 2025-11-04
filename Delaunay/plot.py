import pandas as pd
import matplotlib.pyplot as plt



data=pd.read_csv('delaunay_performance.csv')
plt.plot(data['Points'],data['LiftingMethodSeconds'],marker='o',label='Lifting Method')
plt.plot(data['Points'],data['BowyerWatsonSeconds'],marker='o',label='Bowyer-Watson Method')
plt.xlabel('Number of Points')
plt.ylabel('Time (seconds)')
plt.title('Delaunay Triangulation: Lifting Method vs Bowyer-Watson Method')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("./delaunay_performance/delaunay_performance_comparison.png")
plt.show()