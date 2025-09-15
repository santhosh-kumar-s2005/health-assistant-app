import boto3
import json

# Create a Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def ask_ai(question):
    # Format the prompt for Claude
    prompt = f"\n\nHuman: You are a helpful health assistant. Answer this question: {question}\n\nAssistant:"
    
    # The body for Claude API
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "temperature": 0.2,
        "messages": [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": prompt
            }]
        }]
    })
    
    try:
        
        # Send the request to Claude 3.5 Sonnet
      
        response = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0",  # ✅ correct ID
    body=body,
    accept="application/json",
    contentType="application/json"
)

        
        # Parse the response
        response_body = json.loads(response['body'].read())
        answer = response_body['content'][0]['text']
        return answer
        
    except Exception as e:
        return f"I'm having trouble connecting right now. Error: {str(e)}"