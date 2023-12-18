export type AmplifyDependentResourcesAttributes = {
  "api": {
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
    },
    "uploadUserAudio": {
      "ApiId": "string",
      "ApiName": "string",
      "RootUrl": "string"
    },
    "userAudioAnalysis": {
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
    "audioAnalysisProcessingHandler": {
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
    "userAudioAnalysisHandler": {
      "Arn": "string",
      "LambdaExecutionRole": "string",
      "LambdaExecutionRoleArn": "string",
      "Name": "string",
      "Region": "string"
    },
    "userAudioUploadHandler": {
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
