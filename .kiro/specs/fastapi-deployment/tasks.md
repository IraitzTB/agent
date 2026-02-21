# Implementation Plan: FastAPI Deployment

## Overview

This plan implements a FastAPI REST API layer that wraps the existing GreetingAgent, enabling HTTP-based interaction while maintaining full backward compatibility. The implementation follows a layered architecture with clear separation between API concerns and agent logic.

## Tasks

- [x] 1. Set up project dependencies and structure
  - Add FastAPI, uvicorn, httpx, and hypothesis to dev dependencies using `uv add --dev`
  - Verify existing GreetingAgent tests still pass
  - _Requirements: 1.1, 8.1, 8.4_

- [x] 2. Create Pydantic models for request/response validation
  - [x] 2.1 Create `src/tbbot/models.py` with ChatRequest, ChatResponse, and HealthResponse models
    - Implement ChatRequest with message field validation (min_length=1)
    - Implement ChatResponse with response field
    - Implement HealthResponse with status field (default="healthy")
    - _Requirements: 2.3, 2.4, 3.3_
  
  - [ ]* 2.2 Write property test for request validation
    - **Property 7: Validation Error Handling**
    - **Validates: Requirements 5.1, 5.3**

- [x] 3. Implement FastAPI application and core endpoints
  - [x] 3.1 Create `src/tbbot/api.py` with FastAPI app initialization
    - Initialize FastAPI app with title, description, and version metadata
    - Create GreetingAgent instance
    - _Requirements: 1.1, 1.3, 4.3_
  
  - [x] 3.2 Implement POST /chat endpoint
    - Create async chat endpoint that accepts ChatRequest
    - Call agent.process_message() with request message
    - Return ChatResponse with agent's response
    - Add error handling for internal errors (500 status)
    - _Requirements: 2.1, 2.2, 2.7, 5.4_
  
  - [x] 3.3 Implement GET /health endpoint
    - Create async health endpoint returning HealthResponse
    - Ensure response time is minimal
    - _Requirements: 3.1, 3.2, 3.4_
  
  - [ ]* 3.4 Write property test for API-agent integration consistency
    - **Property 1: API-Agent Integration Consistency**
    - **Validates: Requirements 1.3, 2.2**
  
  - [ ]* 3.5 Write property test for response structure completeness
    - **Property 2: Response Structure Completeness**
    - **Validates: Requirements 2.4**

- [x] 4. Checkpoint - Verify core functionality
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement greeting detection validation
  - [ ]* 5.1 Write property test for greeting detection round-trip
    - **Property 3: Greeting Detection Round-Trip**
    - **Validates: Requirements 2.5, 8.2, 8.3**
  
  - [ ]* 5.2 Write property test for non-greeting response behavior
    - **Property 4: Non-Greeting Response Behavior**
    - **Validates: Requirements 2.6**
  
  - [ ]* 5.3 Write property test for success status code consistency
    - **Property 5: Success Status Code Consistency**
    - **Validates: Requirements 2.7**

- [x] 6. Add CORS support (optional feature)
  - [x] 6.1 Implement configure_cors() function in api.py
    - Add CORS middleware configuration with origins parameter
    - Make CORS disabled by default
    - Support preflight OPTIONS requests
    - _Requirements: 7.1, 7.2, 7.3, 7.4_
  
  - [ ]* 6.2 Write property test for CORS header inclusion
    - **Property 8: CORS Header Inclusion**
    - **Validates: Requirements 7.2**
  
  - [ ]* 6.3 Write unit tests for CORS configuration
    - Test CORS disabled by default
    - Test CORS enabled with headers
    - Test OPTIONS preflight requests
    - _Requirements: 7.1, 7.3, 7.4_

- [ ] 7. Implement comprehensive unit tests with scenario framework
  - [ ]* 7.1 Create `tests/test_api.py` with TestClient-based tests
    - Test POST /chat with greeting messages (hello, hi, hey)
    - Test POST /chat with non-greeting messages
    - Test POST /chat with invalid JSON (422 error)
    - Test POST /chat with missing message field (422 error)
    - Test POST /chat with empty message string (422 error)
    - Test GET /health endpoint returns 200 and correct structure
    - Test GET /docs endpoint availability
    - Test GET /redoc endpoint availability
    - _Requirements: 2.1, 2.5, 2.6, 3.1, 3.2, 4.1, 4.2, 5.1, 5.2, 6.2, 6.3, 6.4_
  
  - [ ]* 7.2 Write property test for health check availability
    - **Property 6: Health Check Availability**
    - **Validates: Requirements 3.2, 3.3**

- [x] 8. Add error handling and logging
  - [x] 8.1 Enhance error handling in chat endpoint
    - Add try-catch for agent processing errors
    - Log errors with appropriate severity levels
    - Return 500 status with generic error message for internal errors
    - _Requirements: 5.4_
  
  - [ ]* 8.2 Write unit tests for error scenarios
    - Test internal agent errors return 500
    - Test error responses include detail field
    - Verify error logging behavior
    - _Requirements: 5.3, 5.4_

- [ ] 9. Verify backward compatibility
  - [ ]* 9.1 Run existing GreetingAgent tests
    - Ensure all existing tests pass without modification
    - Verify agent interface unchanged
    - Verify agent behavior unchanged
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [x] 10. Final checkpoint - Complete validation
  - Run all tests (unit and property-based) with `uv run scenario`
  - Verify API documentation accessible at /docs and /redoc
  - Test manual API interaction with `uvicorn src.tbbot.api:app --reload`
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties using Hypothesis
- Unit tests validate specific examples and edge cases using scenario framework
- CORS support is optional and disabled by default
- Existing GreetingAgent code remains unchanged throughout implementation
- FastAPI provides automatic OpenAPI documentation at /docs and /redoc
