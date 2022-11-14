# UI Integration

After completing the API endpoints and the Cognito part on the backend, follow the steps for the integration in the UI - 

### Setting up the UI Code base
- Navigate to GitHub and [clone the repository](https://github.com/rashmisubhash/fooed-delivery-app) 
- Open the project in your code editor and a new terminal
- `npm install` (installs all the node modules)

### API and Cognito integration in the UI

- Go to *axios.config.js* in the src/crud folder, replace the API and socket *base url* with your *end point* from the API segment
- Go to *UserPool.js* file in the src folder, replace the client_id and UserPoolId with yours from the Cognito segment
- `npm run build` on your terminal - It will optimize, compile, and dump the static files required to serve your application in a build directory. 

## Deploy to S3

The application uses S3 bucket to deploy the web application. Deploying static files requires far fewer moving parts than an app with a server. There’s less to set up and less to maintain. Because there’s less to set up and maintain, the cost of deploying a static application can be dramatically cheaper.

### Create a new S3 bucket

- Create an account or sign in to the [AWS Console](https://aws.amazon.com/)
- Navigate to the S3 service and click on __Create Bucket__. Make up a clever name for your new bucket. In the Set Permissions step, deselect the options to block public access — we want users to access the website assets that will live here.

- Then go ahead and create the bucket.
- Click on the newly-created bucket. Within the Properties, open the Static Website Hosting tab, and select *Use this bucket to host a static website* - fill in index.html for both the Index and Error Documents. By setting index.html as the Error Document, we can allow something like react-router to handle routes outside of the root.

- Open the Permissions tab, then select Bucket Policy. You may choose to do something more nuanced here, but a good starting point is to provide read-only permissions for anonymous users — a policy provided in the AWS examples. 

Note - Make sure its your bucket name under the *Resource* key.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::your-bucket-name/*"
        },
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::your-bucket-name"
        }
    ]
}
```

- Add the contents of your build directory to this bucket. This can be done by clicking on the bucket and clicking Upload. That’s it! You can find the URL to your application back under the Static Website Hosting tab, labeled Endpoint.

### Bonus: Deploying with AWS CLI

You can streamline the deployment process with the AWS Command Line Interface. For example, you might write an npm script to run tests, build the application and push to your S3 bucket. Briefly:

- Create a user with security credentials in IAM. Avoid providing more permissions than is necessary.
- Configure the CLI with aws configure. For example:

```
AWS Access Key ID [None]: Your Access key
AWS Secret Access Key [None]: Your Secret Access key
Default region name [None]: us-west-2
Default output format [None]: json
```

- Deploy your app with the following command (using the bucket name)

__Note__ - If any changes are present in your local branch, build your app before you deploy, if not directly deploy it. 

```
// build and deploy the app
npm run build && aws s3 sync build/ s3://your-bucket-name

// deploy the app
aws s3 sync build/ s3://your-bucket-name`
```

The deploy script above is as simple as it gets. It takes the contents of the build directory (produced by npm run build) and replaces whatever is currently in your bucket with those contents.

## Deploy to CloudFront

If it works on S3, why bother with CloudFront?

CloudFront is the Content Delivery Network (CDN) service offered by AWS. CDNs optimize for speed by pushing your content out to edge locations, making it highly available around the globe. If your users are only local, the performance offered by S3 may be just fine.

### Follow the steps below

- Select the CloudFront service in the AWS console, click Create Distribution, then under the web delivery method, click Get Started.

- Select your Origin Settings. The Origin Domain Name choices pre-populate with S3 buckets. Selecting yours will also populate the Origin ID.

- Set the Default Root Object to index.html

- Click on __Create Distribution__

- Click the ID of your newly created distribution to reach its settings page, then click on the Error Pages tab. Select Create Custom Error Response.
- Select Yes for a custom error response, set/index.html for the response page path and 200: OK for the response code. This custom error page in the CloudFront distribution is analogous to the Error Document on the S3 bucket (and will work on IE, too). When done, click Create.

That’s it! Give the deployment a handful of minutes, then check out your web app. You can find the URL on the distribution listings page, under the Domain Name column.
