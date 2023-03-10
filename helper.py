import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(scores, mean_scores):
    """
    Plots the scores and mean scores of the training process.

    Args:
    - scores: a list of the scores obtained in each game during training
    - mean_scores: a list of the mean scores obtained at each point during training

    Returns: None
    """
    # Clear the current display
    display.clear_output(wait=True)

    # Display the current plot
    display.display(plt.gcf())

    # Clear the plot
    plt.clf()

    # Add the plot title and axis labels
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')

    # Add the scores and mean scores to the plot
    plt.plot(scores)
    plt.plot(mean_scores)

    # Set the y-axis minimum value to 0
    plt.ylim(ymin=0)

    # Add the latest scores and mean scores to the plot
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

    # Show the plot without blocking and pause for a short amount of time
    plt.show(block=False)
    plt.pause(.1)
