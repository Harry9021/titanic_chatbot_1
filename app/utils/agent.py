import os
import pandas as pd
import sys
from langchain.agents import AgentType, initialize_agent, Tool
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.tools import tool
from langchain_openai import OpenAI

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.utils.data_loader import load_titanic_dataset

class TitanicAgent:
    def __init__(self, api_key=None):
        # Use provided API key or try to get from environment
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        
        # If no API key is available, we'll use an alternative approach
        # by constructing simple responses based on predefined queries
        if not self.api_key:
            print("Warning: No OpenAI API key found. Using simplified query processing.")
            self.agent = None
            self.df = load_titanic_dataset()
        else:
            # Initialize the LLM
            llm = OpenAI(openai_api_key=self.api_key, temperature=0)
            
            # Define tools for the agent
            tools = [
                Tool(
                    name="PassengerQuery",
                    func=self.query_passengers,
                    description="Useful for answering questions about Titanic passengers, their demographics, survival rates, and other statistics."
                )
            ]
            
            # Initialize the agent
            self.agent = initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )
    
    def query_passengers(self, query):
        """Execute a query on the Titanic dataset"""
        df = load_titanic_dataset()
        
        # Try to interpret the query as a pandas operation
        try:
            # This is a simplified approach and would need robust security measures in production
            # For demonstration purposes only
            result = eval(f"df.{query}")
            if isinstance(result, pd.DataFrame):
                return result.to_string()
            else:
                return str(result)
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def process_query(self, query):
        """Process a natural language query about the Titanic dataset"""
        # If we have an agent, use it
        if self.agent:
            try:
                response = self.agent.run(query)
                return {
                    "answer": response,
                    "visualization_type": self._determine_visualization(query),
                    "success": True
                }
            except Exception as e:
                return {
                    "answer": f"Error processing query: {str(e)}",
                    "visualization_type": None,
                    "success": False
                }
        
        # If no agent, use simple keyword matching
        else:
            return self._simple_query_processor(query)
    
    def _simple_query_processor(self, query):
        """Simple keyword-based query processor as a fallback"""
        query = query.lower()
        
        # Different query patterns
        if "percentage" in query and "male" in query:
            male_percentage = (self.df['Sex'] == 'male').mean() * 100
            return {
                "answer": f"{male_percentage:.2f}% of passengers were male on the Titanic.",
                "visualization_type": "gender_distribution",
                "success": True
            }
        
        elif "histogram" in query and "age" in query:
            return {
                "answer": "Here's a histogram showing the distribution of passenger ages.",
                "visualization_type": "age_histogram",
                "success": True
            }
        
        elif "average" in query and "fare" in query:
            avg_fare = self.df['Fare'].mean()
            return {
                "answer": f"The average ticket fare was ${avg_fare:.2f}.",
                "visualization_type": "fare_histogram",
                "success": True
            }
        
        elif "embark" in query or "port" in query:
            port_counts = self.df['Embarked'].value_counts()
            port_mapping = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}
            port_info = ", ".join([f"{port_mapping.get(port, port)}: {count}" for port, count in port_counts.items()])
            
            return {
                "answer": f"Passengers embarked from the following ports: {port_info}",
                "visualization_type": "embarkation_count",
                "success": True
            }
        
        elif "survival" in query and ("class" in query or "pclass" in query):
            return {
                "answer": "Here's the survival rate breakdown by passenger class.",
                "visualization_type": "survival_by_class",
                "success": True
            }
        
        elif "survival" in query or "survived" in query:
            survival_count = self.df['Survived'].sum()
            total = len(self.df)
            survival_rate = (survival_count / total) * 100
            
            return {
                "answer": f"{survival_count} passengers survived out of {total}, a survival rate of {survival_rate:.2f}%.",
                "visualization_type": "survival_count",
                "success": True
            }
        
        else:
            return {
                "answer": "I'm not sure how to answer that question about the Titanic dataset. Try asking about passenger demographics, survival rates, ticket fares, or embarkation ports.",
                "visualization_type": None,
                "success": False
            }
    
    def _determine_visualization(self, query):
        """Determine which visualization to show based on the query"""
        query = query.lower()
        
        if "age" in query and ("histogram" in query or "distribution" in query):
            return "age_histogram"
        elif "fare" in query and ("histogram" in query or "distribution" in query):
            return "fare_histogram"
        elif "gender" in query or "male" in query or "female" in query:
            return "gender_distribution"
        elif "embark" in query or "port" in query:
            return "embarkation_count"
        elif "class" in query and "survival" in query:
            return "survival_by_class"
        elif "survival" in query or "survived" in query:
            return "survival_count"
        elif "correlation" in query:
            return "correlation_heatmap"
        elif "age" in query and "fare" in query:
            return "age_vs_fare"
        
        return None