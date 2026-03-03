# Implementation Plan: Greeting Agent

## Overview

This plan implements TBBot's multilingual greeting agent functionality using Python and the Agno framework. The implementation follows a simple pipeline pattern: detect greetings in student messages (supporting English, Catalan, Basque, and Galician), coordinate processing through an Agno agent handler, and generate standardized responses in the appropriate language. Tasks are organized to build incrementally, starting with core multilingual detection logic, then agent orchestration, and finally integration with testing.

## Tasks

- [x] 1. Set up project structure and core modules
  - Create `src/tbbot/` directory structure
  - Create `__init__.py` files for package structure
  - Create `src/tbbot/greeting.py` for greeting functionality
  - Set up `tests/` directory with `__init__.py`
  - _Requirements: 3.1, 3.2_

- [x] 2. Implement greeting detection logic
  - [x] 2.1 Implement `detect_greeting()` function
    - Write function that returns tuple of (is_greeting, language_code)
    - Support multilingual detection: English ("hello", "hi", "hey"), Catalan ("hola"), Basque ("kaixo"), Galician ("ola")
    - Perform case-insensitive keyword matching with language priority
    - Handle empty strings and None inputs gracefully
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [x] 2.2 Write unit tests for greeting detection
    - Test each English greeting keyword ("hello", "hi", "hey") returns ('en')
    - Test multilingual greetings: "hola" ('ca'), "kaixo" ('eu'), "ola" ('gl')
    - Test case-insensitivity for all languages (e.g., "HELLO", "HOLA", "KAIXO")
    - Test non-greeting messages return (False, None)
    - Test edge cases (empty string, whitespace, mixed content)
    - Test language priority when multiple greetings present
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [x] 3. Implement response generator
  - [x] 3.1 Implement `generate_greeting_response()` function
    - Accept language_code parameter ('en', 'ca', 'eu', 'gl')
    - Return appropriate greeting message for each language:
      - English: "Hi, my name is TBBot. I am here to help you with your questions"
      - Catalan: "Hola, el meu nom és TBBot. Estic aquí per ajudar-te amb les teves preguntes"
      - Basque: "Kaixo, nire izena TBBot da. Hemen nago zure galderekin laguntzeko"
      - Galician: "Ola, o meu nome é TBBot. Estou aquí para axudarche coas túas preguntas"
    - _Requirements: 2.1, 5.1, 5.2, 5.3, 5.5_
  
  - [x] 3.2 Write unit tests for response generator
    - Verify exact response text matches specification for each language
    - Test all supported language codes ('en', 'ca', 'eu', 'gl')
    - _Requirements: 2.1, 5.1, 5.2, 5.3, 5.5_

- [x] 4. Implement data models
  - [x] 4.1 Create Message and Response dataclasses
    - Define `Message` dataclass with content and timestamp fields
    - Define `Response` dataclass with content and timestamp fields
    - Add type hints for all fields
    - _Requirements: 4.2, 4.3_
  
  - [ ]* 4.2 Write unit tests for data models
    - Test Message creation and field access
    - Test Response creation and field access
    - Test timestamp generation
    - _Requirements: 4.2, 4.3_

- [x] 5. Checkpoint - Verify core components
  - Ensure all tests pass, ask the user if questions arise.

- [x] 6. Implement Agno agent handler
  - [x] 6.1 Create `GreetingAgent` class with Agno integration
    - Implement `__init__()` method to initialize Agno framework
    - Add error logging for initialization failures
    - Implement `process_message()` method to coordinate detection and response
    - Use `detect_greeting()` to detect greetings and get language code
    - Use `generate_greeting_response()` with detected language for greeting responses
    - Return empty string for non-greeting messages
    - _Requirements: 3.1, 3.2, 3.3, 4.1, 2.1, 2.3, 5.5_
  
  - [x] 6.2 Write unit tests for GreetingAgent
    - Test agent initialization
    - Test English greeting message processing returns correct response
    - Test multilingual greeting processing (Catalan, Basque, Galician) returns correct responses
    - Test non-greeting message processing returns empty string
    - Test multiple message processing in order
    - _Requirements: 3.1, 3.2, 4.1, 2.1, 2.3, 5.1, 5.2, 5.3, 5.5, 6.1, 6.2_

- [x] 7. Add integration and entry point
  - [x] 7.1 Create main entry point (if needed)
    - Create `src/main.py` or similar entry point for running the agent
    - Initialize GreetingAgent
    - Add basic message loop or CLI interface for testing
    - _Requirements: 3.1, 3.2_
  
  - [ ]* 7.2 Write integration tests
    - Test end-to-end greeting flow using scenario framework for all languages
    - Test agent responds to multilingual greetings within acceptable time
    - Test agent handles multiple sequential messages correctly
    - Test language-specific responses match requirements
    - _Requirements: 2.2, 4.1, 5.1, 5.2, 5.3, 5.5, 6.1, 6.2_

- [x] 8. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- The implementation uses Python with the Agno framework as specified in the design
- Testing uses the scenario framework as specified in requirements
- Multilingual support includes English, Catalan, Basque, and Galician languages
- Language detection follows priority order with first match determining response language
- Checkpoints ensure incremental validation at logical breakpoints
