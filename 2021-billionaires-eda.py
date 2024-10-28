import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Line 1
def clean_net_worth(data):
    """
    Cleans the 'wealth.worth in billions' column by converting it to numeric values
    and handling NaN values.
    """
    # Line 7
    # Convert the 'wealth.worth in billions' column to numeric
    data["TotalNetWorth"] = pd.to_numeric(
        data["wealth.worth in billions"], errors="coerce"
    )

    # Line 11
    # Drop rows with NaN values in the 'TotalNetWorth' column
    data = data.dropna(subset=["TotalNetWorth"])

    return data


# Line 16
def plot_stacked_histogram(data, x_var, groupby_var):
    """
    Plots a stacked histogram for the specified x variable grouped by the groupby_var column.
    """
    # Line 21
    # Ensure the groupby_var column contains only strings (to avoid mixed types)
    data[groupby_var] = data[groupby_var].astype(str)

    # Line 25
    df_agg = data.loc[:, [x_var, groupby_var]].groupby(groupby_var)
    vals = [data_[x_var].values.tolist() for i, data_ in df_agg]

    # Line 29
    # Create the plot
    plt.figure(figsize=(20, 8), dpi=80)
    colors = [plt.cm.Pastel1(i / float(len(vals) - 1)) for i in range(len(vals))]

    # Line 34
    # Plot the histogram
    n, bins, patches = plt.hist(
        vals, 30, stacked=True, density=False, color=colors[: len(vals)]
    )

    # Line 39
    # Add a legend
    plt.legend(
        {
            group: col
            for group, col in zip(
                np.unique(data[groupby_var]).tolist(), colors[: len(vals)]
            )
        }
    )

    # Line 46
    # Customize the plot
    plt.title(f"Stacked Histogram of {x_var} colored by {groupby_var}", fontsize=22)
    plt.xlabel(x_var)
    plt.ylabel("Frequency")
    plt.xticks(ticks=bins[::3], labels=[round(b, 1) for b in bins[::3]])
    plt.show()


# Line 54
def plot_scatterplot(data, x_var, y_var, color_by_var=None, size_by_var=None):
    """
    Plots a scatterplot of two variables and optionally colors/sizes points
    by other variables.
    """
    plt.figure(figsize=(10, 6))

    # Line 60
    if color_by_var:
        unique_groups = data[color_by_var].unique()
        colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_groups)))
        for color, group in zip(colors, unique_groups):
            subset = data[data[color_by_var] == group]
            plt.scatter(subset[x_var], subset[y_var], label=group, color=color)
        plt.legend()
    else:
        plt.scatter(data[x_var], data[y_var])

    # Line 70
    plt.title(f"Scatterplot of {x_var} vs {y_var}")
    plt.xlabel(x_var)
    plt.ylabel(y_var)

    # Line 74
    if size_by_var:
        sizes = np.log(data[size_by_var].fillna(1)) * 100
        plt.scatter(data[x_var], data[y_var], s=sizes)

    plt.show()


# Line 80
def describe_data(data):
    """
    Provides basic descriptive statistics and missing value analysis for the dataset.
    """
    print("Basic Info:")
    print(data.info())

    print("\nDescriptive Statistics:")
    print(data.describe(include="all"))

    print("\nMissing Values:")
    print(data.isnull().sum())


# Line 91
def main():
    """
    Main function to load the data, clean it, and run exploratory data analysis (EDA).
    """
    # Load the dataset
    file_path = "data/billionaires.csv"  # Update this to your file path
    data = pd.read_csv(file_path)

    # Clean the data
    data = clean_net_worth(data)

    # Describe the data
    describe_data(data)

    # Plot a stacked histogram of TotalNetWorth grouped by 'company.sector'
    plot_stacked_histogram(data, x_var="TotalNetWorth", groupby_var="company.sector")

    # Plot a scatterplot of age vs TotalNetWorth, colored by 'demographics.gender'
    plot_scatterplot(
        data,
        x_var="demographics.age",
        y_var="TotalNetWorth",
        color_by_var="demographics.gender",
    )


# Line 110
if __name__ == "__main__":
    main()
