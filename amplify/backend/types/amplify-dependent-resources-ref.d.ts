export type AmplifyDependentResourcesAttributes = {
  "api": {
    "analysisGenerationFromAudio": {
      "ApiId": "string",
      "ApiName": "string",
      "RootUrl": "string"
    },
    "cvService": {
      "ApiId": "string",
      "ApiName": "string",
      "RootUrl": "string"
    },
    "cvServiceProcessed": {
      "ApiId": "string",
      "ApiName": "string",
      "RootUrl": "string"
    },
    "questionGeneration": {
      "ApiId": "string",
      "ApiName": "string",
      "RootUrl": "string"
    }
  },
  "auth": {
    "weprep1538f8ae": {
      "AppClientID": "string",
      "AppClientIDWeb": "string",
      "IdentityPoolId": "string",
      "IdentityPoolName": "string",
      "UserPoolArn": "string",
      "UserPoolId": "string",
      "UserPoolName": "string"
    }
  },
  "function": {
    "audioAnalysisHandler": {
      "Arn": "string",
      "LambdaExecutionRole": "string",
      "LambdaExecutionRoleArn": "string",
      "Name": "string",
      "Region": "string"
    },
    "cvServiceHandler": {
      "Arn": "string",
      "LambdaExecutionRole": "string",
      "LambdaExecutionRoleArn": "string",
      "Name": "string",
      "Region": "string"
    },
    "cvServiceProcessingHandler": {
      "Arn": "string",
      "LambdaExecutionRole": "string",
      "LambdaExecutionRoleArn": "string",
      "Name": "string",
      "Region": "string"
    },
    "questionGenerationHandler": {
      "Arn": "string",
      "LambdaExecutionRole": "string",
      "LambdaExecutionRoleArn": "string",
      "Name": "string",
      "Region": "string"
    },
    "userCVProcessing": {
      "Arn": "string",
      "LambdaExecutionRole": "string",
      "LambdaExecutionRoleArn": "string",
      "Name": "string",
      "Region": "string"
    }
  },
  "storage": {
    "userCV": {
      "BucketName": "string",
      "Region": "string"
    }
  }
}
