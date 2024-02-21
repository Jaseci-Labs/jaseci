import sys
import os

repo_path = "home\jayanaka-98\dspy"
if repo_path not in sys.path:
    sys.path.append(repo_path)

os.environ["DSP_NOTEBOOK_CACHEDIR"] = os.path.join(repo_path, 'cache')

import pkg_resources # Install the package if it's not installed
if not "dspy-ai" in {pkg.key for pkg in pkg_resources.working_set}:
    !pip install -U pip
    !pip install dspy-ai
    !pip install openai~=0.28.1
    # !pip install -e $repo_path

import dspy

turbo = dspy.OpenAI(model='gpt-3.5-turbo')
colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')


class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question: dspy.InputField = _Jac.has_instance_default(gen_func=lambda : dspy.InputField())
    answer: dspy.OutputField = _Jac.has_instance_default(gen_func=lambda : dspy.OutputField(desc='often between 1 and 5 words'))

dspy.settings.configure(lm=turbo, rm=colbertv2_wiki17_abstracts)
generate_answer = dspy.Predict(BasicQA)
pred = generate_answer(question='What is the capital of France?')
print(pred)