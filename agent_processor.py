import warnings
from typing import List, Tuple, Any
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from config import AgentConfig


warnings.filterwarnings('ignore')

class AgentProcessor:
    """Handles all agent-related processing and content generation"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = self._setup_llm()
        self.search_tool = SerperDevTool()
        
    def _setup_llm(self) -> LLM:
        """Initialize the Language Learning Model"""
        return LLM(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
    
    def _create_agents(self) -> List[Agent]:
        """Create all required agents"""
        researcher = Agent(
            role='Company Researcher',
            goal='Research companies and gather relevant information.',
            tools=[self.search_tool],
            backstory="Expert researcher for company information.",
            llm=self.llm,
            verbose=True
        )
        
        analyst = Agent(
            role='Technical Analyst',
            goal='Analyze and refine the information gathered by the researcher into a concise summary.',
            backstory="You are a technical analyst with expertise in interpreting financial data and trends.",
            llm=self.llm,  # Assign the LLM to the agent
            verbose=True
)
        
        podcaster = Agent(
            role='Podcast Creator',
            goal='Create an engaging podcast script based on the analyzed information, including questions and jokes.',
            backstory="You are a creative podcast host who turns complex information into entertaining and informative content.",
            llm=self.llm,  # Assign the LLM to the agent
            verbose=True
)
        
        return [researcher, analyst, podcaster]
    
    def _create_tasks(self, agents: List[Agent]) -> List[Task]:
        """Create tasks for the agents"""
        return [
            Task(
                description='Research the following companies: {companies}. Gather detailed information on stock prices, trends, news, and other relevant metrics.',
                agent=agents[0],
                expected_output='''A detailed report on each company including:
                - Stock price
                - Stock trend
                - Dividends
                - Market cap
                - Next financial earnings
                - Trending news (at least 1 minute worth of reading material)'''
            ),
            Task(
                description='Analyze the research data and refine it into a concise summary. Highlight key trends, insights, and notable events.',
                agent=agents[1],
                expected_output='A refined summary of the research data, highlighting key points and trends.'
            ),
            Task(
                description='''Create a podcast script based on the analyzed data. Include interesting questions, jokes, and a conversational tone.
                The script should be structured as a list of tuples, where each tuple contains the speaker's role and their dialogue.
                Example format:
                [
                    ("Host", "Welcome to our podcast! Today, we're discussing Apple's recent stock performance."),
                    ("Guest", "Thanks for having me! Apple's stock is currently trading at around $245.55."),
                    ("Host", "That's impressive growth. What's driving this bullish trend?"),
                    ("Guest", "The stock's bullish trend is supported by strong upward momentum."),
                    ...
                ]
                Ensure the script is engaging, informative, and entertaining.''',
                agent=agents[2],
                expected_output='''A podcast script structured as a list of tuples, where each tuple contains the speaker's role and their dialogue. Example:
                [
                    ("Host", "Welcome to our podcast! Today, we're discussing Apple's recent stock performance."),
                    ("Guest", "Thanks for having me! Apple's stock is currently trading at around $245.55."),
                    ("Host", "That's impressive growth. What's driving this bullish trend?"),
                    ("Guest", "The stock's bullish trend is supported by strong upward momentum."),
                    ...
                ]'''
            )
        ]
    
    def process_companies(self, companies: List[str]) -> List[Tuple[str, str]]:
        """Process company information and generate podcast script"""
        agents = self._create_agents()
        tasks = self._create_tasks(agents)
        
        crew = Crew(
            agents=agents,
            tasks=tasks,
            verbose=True
        )
        
        result = crew.kickoff(inputs={'companies': companies})
        return self._convert_output_to_list(result)
    
    @staticmethod
    def _convert_output_to_list(output: Any) -> List[Tuple[str, str]]:
        """Convert crew output to list of tuples"""
        if isinstance(output, list):
            return output
        
        output_str = str(output)
        cleaned_str = output_str.replace('```python', '').replace('```', '').strip()
        try:
            return eval(cleaned_str)
        except Exception as e:
            print(f"Error converting output: {e}")
            return []
