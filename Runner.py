
# %%
import OptionEvaluator
#importlib.reload(OptionEvaluator)
Evaluator = OptionEvaluator.Evaluator()

# %%
ticker = 'SPY'
Evaluator.getQuote(ticker)



# %%
Evaluator.getGraph(ticker)


# %%
Evaluator.screenCC()

# %%
Evaluator.getOptions('SPY')