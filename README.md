# STEM ESSAY Readme 🚀

[![standard-readme compliant](https://img.shields.io/badge/readme%20-KAKU-brightgreen.svg?style=flat-square)](https://github.com/YiVal/Kaku/blob/master/README.md)

🔥 Feb 18: STEM ESSAY is first created in [YiVal](https://github.com/YiVal)

🔥 For more in-depth information and resources, please visit our [official website](https://stemessay.com/).


## What is STEM ESSAY? 🤖

STEM ESSAY is a cutting-edge tool designed to simplify the process of creating structured outlines for STEM essays. It uses advanced algorithms to break down complex topics into coherent, logically organized outlines, making essay writing in Science, Technology, Engineering, and Mathematics fields more accessible and less time-consuming.

Our goal is to help users from students to researchers transform their ideas into high-quality essays with ease. STEM ESSAY supports a wide range of STEM disciplines, ensuring your essays are structured, insightful, and ready to engage your audience. It's not just an aid; it's your companion in mastering STEM writing! 🌟

### Problems STEM ESSAY Tries to Tackle 🛠️

- **Complexity Simplification:** Breaks down intricate STEM topics into manageable outlines.
- **Time Efficiency:** Reduces the hours spent on structuring essays.
- **Clarity and Coherence:** Enhances the readability of STEM essays for a wider audience.
- **Idea Organization:** Helps organize thoughts and research findings systematically.
- **Writing Barriers:** Lowers the entry barrier for effective STEM communication.


## Install

### Requirements

- Linux
- Python 3.10+
- [openai](https://github.com/openai)
- [pyautogen](https://github.com/microsoft/autogen)


a. Clone the project.

```shell
git clone https://github.com/YiVal/Kaku

cd Kaku
```

b. Create a conda virtual environment and activate it.

```shell
conda create -n kaku python=3.10 -y

conda activate kaku
```

c. Install dependencies.

```shell
pip install -r requirements.txt
```


## Usage

You should obtain an APl key from OpenAl. Once you have the key, set it as an environment variable named OPENAI API KEY.


**Set OpenAI API Key**: Replace `$YOUR_OPENAI_API_KEY` with your
   actual OpenAI API key.

   On macOS or Linux systems,

   ```bash
   export OPENAI_API_KEY=$YOUR_OPENAI_API_KEY
   ```

   On Windows systems,

   ```powershell
   setx OPENAI_API_KEY $YOUR_OPENAI_API_KEY
   ```
For example:
```sh
export OPENAI_API_KEY='sk...DAHY'
```


You can then run the code using the following command:
```sh
cd src/

python test.py
```

The first step in the automated essay generation process is to generate a topic. Then you will get the result
```sh
[DEBUG] Topics: 
1. "Analyzing the Impact and Efficiency of Different Voting Systems through Mathematical Modelling"
2. "A Comprehensive Study about the Probability and Statistical Implications in Casino Games"
3. "The Application and Effectiveness of Cryptography in Digital Security: A Mathematical Perspective"
select one of the topic.. 
```
With the topic selected, the next step is to generate an outline. 
```sh
Admin (to chat_manager):

Write an IB essay "Evaluating the Efficiency and Impact of Cryptographic Algorithms in Cybersecurity: A Mathematical Analysis" with 4000 words.

--------------------------------------------------------------------------------
subject_expert (to chat_manager):

[plan]
Title: Evaluating the Efficiency and Impact of Cryptographic Algorithms in Cybersecurity: A Mathematical Analysis

1. Introduction/Rationale (Word Count: 300)
- Purpose: To explore the significance of cryptographic algorithms in the digital age where cybersecurity threats are omnipresent, and to understand and evaluate their mathematical complexities and efficacies.
- Personal Motivation: Recount a scenario wherein the breach of personal data led to a growing concern over cybersecurity and a fascination with the cryptographic measures employed for protection. This intrigue fueled a deeper look into the underlying mathematics of these cryptographic systems.
- Research Objective: To quantitatively analyze and assess the efficiency and impact of various cryptographic algorithms, with a focus on their computational complexity, security level, and practical performance in cybersecurity applications.

2. Background Information (Word Count: 500)
...
```
The final step is the actual writing of the essay based on the generated outline. The following is a partial paragraph display

```sh
Admin (to chat_manager):

Write the following paragraph:
 1.Introduction/Rationale
pose: To explore the significance of cryptographic algorithms in the digital age where cybersecurity threats are omnipresent, and to understand and evaluate their mathematical complexities and efficacies.
sonal Motivation: Recount a scenario wherein the breach of personal data led to a growing concern over cybersecurity and a fascination with the cryptographic measures employed for protection. This intrigue fueled a deeper look into the underlying mathematics of these cryptographic systems.
earch Objective: To quantitatively analyze and assess the efficiency and impact of various cryptographic algorithms, with a focus on their computational complexity, security level, and practical performance in cybersecurity applications. 
 total words:300
...
In the vibrant realm of casino games, understanding the dance of chance is paramount. At its core lies probability theory, a branch of mathematics that navigates through the potential outcomes in games of chance. It all begins with a well-defined set of possibilities, known as the sample space, and the events or outcomes that may occur within it. The probability of an event is simply the count of favorable outcomes divided by the total number of outcomes - a formula elegantly captured by \( P(E) = \frac{n(E)}{n(S)} \).

Random variables come into play when outcomes are numerical, such as the dots facing up after a dice toss. These variables allow us to calculate predicted results or 'expected values'. The expected value—what one might anticipate in the long run—is found by weighting each possible outcome by its corresponding probability and summing them up: \( E(X) = \sum (x_i \cdot P(x_i)) \).

Another vital tool is variance, which captures how much the outcomes spread out from the expected value. It's described mathematically by \( Var(X) = E((X - E(X))^2) \), offering a gauge of a game's risk level. The square root of variance, the standard deviation, is especially handy as it measures risk in the original units of the data.

Statistical independence is the notion that one event doesn't influence another, essential when dealing with sequential actions, such as separate draws from a deck of cards. Independence is central to correctly calculating combined event probabilities, a frequent aspect of gaming strategies.

The binomial distribution allows us to predict outcomes for a specific number of successes in a series of independent trials, such as betting on red in roulette several times. It's a model that exemplifies the predictability embedded within supposedly random events.

Probability distributions chart all the potential outcomes for a variable and their likelihoods, summing up to 1. These can be discrete or continuous, painting a picture of what to expect from a game on any given play.

Breaking down these foundational concepts, such as random variables, expected value, variance, statistical independence, and binomial distribution, and applying probability to sample spaces in games of chance, we can interpret the erratic nature of games into more measured elements. This treatment not only deepens our strategic understanding but creates a bridge from abstract math to the tangible decisions made at the tables and slot machines.
...

```

The following shows the images generated by the essay：

<p align="center">
  <img src="src/pdffile/src/image_3_2_1.png" width="500" alt="Example Image">
</p>
<p align="center">
  <img src="src/pdffile/src/image_3_2_2.png" width="500" alt="Example Image">
</p>
<p align="center">
  <img src="src/pdffile/src/image_3_3_1.png" width="500" alt="Example Image">
</p>




The following represents a selection of essay topics that can be generated. If you're interested in using our project, you can follow the example provided in 

| Topic | Notebook Link |
|-------|---------------|
| Understanding the Role of Probability Theory and Statistics in Predictive Modeling for Climate Change Scenarios| [![Notebook - Topic 1](https://img.shields.io/badge/Notebook-Topic1-bule.svg?style=flat-square)](https://github.com/YiVal/Kaku/blob/master/src/notebook/essay_topic_1.ipynb) |
| The Mathematical Exploration of Population Growth: An investigation into different types of mathematical models predicting population growth over time | [![Notebook - Topic 2](https://img.shields.io/badge/Notebook-Topic2-bule.svg?style=flat-square)](https://github.com/YiVal/Kaku/blob/master/src/notebook/essay_topic_2.ipynb) |
| Predicting Stock Market Trends Using Stochastic Processes and Probability Theory| [![Notebook - Topic 3](https://img.shields.io/badge/Notebook-Topic3-bule.svg?style=flat-square)](https://github.com/YiVal/Kaku/blob/master/src/notebook/essay_topic_3.ipynb) |

## Stem Essay Use Case: Modeling of Zombie Apocalypse

<a href="https://www.youtube.com/watch?app=desktop&v=UxKIGGPOt4c&feature=youtu.be">
    <img src="http://img.youtube.com/vi/UxKIGGPOt4c/0.jpg" alt="Demo" width="800"/>
</a>



## Contributing


This project is open to contributions and ideas. To contribute, you'll need to accept a Contributor License Agreement (CLA), which confirms your authority to offer your contribution and grants us the permission to utilize it.

Upon initiating a pull request, an automated CLA system will assess if your contribution requires a CLA and update the pull request with the necessary information (such as a status check or a comment). Just follow the steps outlined by the automated system. This process is a one-time requirement for all contributions across repositories that employ our CLA.

### Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/YiVal/YiVal/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=YiVal/YiVal" />
</a>

## Contact Us

<p align="center">
  <a href="https://www.facebook.com/profile.php?id=61555698471344" style="margin-right: 20px;"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-facebook.png" alt="Facebook" style="width: 60px;"/></a>
  <a href="https://www.instagram.com/stemessay/" style="margin-right: 20px;"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-instagram.png" alt="Instagram" style="width: 60px;"/></a>
  <a href="https://twitter.com/EssayStem93096" style="margin-right: 20px;"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-twitter.png" alt="Twitter" style="width: 60px;"/></a>
  <a href="https://github.com/YiVal/Kaku" style="margin-right: 20px;"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-github.png" alt="Github" style="width: 60px;"/></a>
  <a href="https://www.youtube.com/@KaKoolove"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-youtube.png" alt="Youtube" style="width: 60px;"/></a>
  <a href="https://weibo.com/7893235440/O1QmBoq9Q" style="margin-right: 20px;"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-weibo.png" alt="Weibo" style="width: 60px;"/></a>
  <a href="https://www.xiaohongshu.com/user/profile/652d33220000000002013ef6" style="margin-right: 20px;"><img src="https://github.com/YiVal/Kaku/blob/master/social/logo-social-xiaohongshu.png" alt="Xiaohongshu" style="width: 60px;"/></a>
</p>


## License

MIT 
