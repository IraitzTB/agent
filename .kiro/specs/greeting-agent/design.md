# Design Document: Greeting Agent

## Overview

The greeting agent is TBBot's first functional capability, providing a foundation for student-agent interaction. The agent detects greeting messages from students and responds with a standardized introduction. This design implements a simple pattern-matching approach using the Agno framework for agent orchestration.

The system consists of three main components:
1. A greeting detector that identifies greeting keywords in student messages
2. An agent handler that processes messages and coordinates responses
3. A response generator that produces the standardized greeting message

This minimal design establishes the architectural patterns that will be extended for future TBBot capabilities.

## Architecture

### System Context

```mermaid
graph LR
    Student[Student] -->|Text Message| TBBot[TBBot Agent]
    TBBot -->|Text Response| Student
```

### Component Architecture

```mermaid
graph TD
    Input[Student Message] --> Agent[Agno Agent Handler]
    Agent --> Detector[Greeting Detector]
    Detector -->|Is Greeting?| Decision{Greeting Detected?}
    Decision -->|Yes| Generator[Response Generator]
    Decision -->|No| NoOp[No Response]
    Generator --> Output[Greeting Response]
```

The architecture follows a simple pipeline pattern:
- **Input Layer**: Receives text messages from students
- **Processing Layer**: Detects greetings using keyword matching
- **Output Layer**: Generates standardized greeting responses

### Technology Stack

- **Agent Framework**: Agno (Python-based agent orchestration)
- **Language**: Python 3.x
- **Testing**: scenario framework for unit tests
- **Dependency Management**: uv

## Components and Interfaces

### 1. Greeting Detector

**Purpose**: Identifies whether a student message contains a greeting and determines the language

**Interface**:
```python
def detect_greeting(message: str) -> tuple[bool, str | None]:
    """
    Detects if a message contains a greeting keyword and identifies the language.
    
    Args:
        message: The student's input message
        
    Returns:
        Tuple of (is_greeting, language_code) where language_code is one of:
        'en' (English), 'ca' (Catalan), 'eu' (Basque), 'gl' (Galician), or None
    """
```

**Implementation Strategy**:
- Convert message to lowercase for case-insensitive matching
- Check for presence of greeting keywords in priority order
- Return both detection result and detected language
- Language detection is mutually exclusive (first match wins)

**Keywords by Language**:
- English: ["hello", "hi", "hey"]
- Catalan: ["hola"]
- Basque: ["kaixo"]
- Galician: ["ola"]

### 2. Agno Agent Handler

**Purpose**: Orchestrates message processing using the Agno framework

**Interface**:
```python
class GreetingAgent:
    """
    TBBot agent that handles greeting detection and response.
    """
    
    def __init__(self):
        """Initialize the agent with Agno framework."""
        
    def process_message(self, message: str) -> str:
        """
        Process a student message and return appropriate response.
        
        Args:
            message: The student's input message
            
        Returns:
            Response string (greeting or empty)
        """
```

**Responsibilities**:
- Initialize Agno agent framework
- Receive student messages
- Coordinate greeting detection
- Return appropriate responses
- Handle initialization errors with logging

### 3. Response Generator

**Purpose**: Produces the appropriate greeting response based on detected language

**Interface**:
```python
def generate_greeting_response(language_code: str) -> str:
    """
    Generate the TBBot greeting message in the specified language.
    
    Args:
        language_code: Language code ('en', 'ca', 'eu', 'gl')
        
    Returns:
        The greeting response string in the specified language
    """
```

**Response Formats by Language**:
- English ('en'): "Hi, my name is TBBot. I am here to help you with your questions"
- Catalan ('ca'): "Hola, el meu nom és TBBot. Estic aquí per ajudar-te amb les teves preguntes"
- Basque ('eu'): "Kaixo, nire izena TBBot da. Hemen nago zure galderekin laguntzeko"
- Galician ('gl'): "Ola, o meu nome é TBBot. Estou aquí para axudarche coas túas preguntas"

## Data Models

### Message

```python
@dataclass
class Message:
    """Represents a student message."""
    content: str
    timestamp: float
```

### Response

```python
@dataclass
class Response:
    """Represents an agent response."""
    content: str
    timestamp: float
```

These simple data models provide structure for message handling and can be extended for future features (e.g., message IDs, conversation context).

