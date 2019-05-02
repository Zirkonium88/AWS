# Loading data via functional user from a DynamoDB

Sometimes you need dynamic content on a static website. Within AWS, this can be done with the [AWS SDK for JavaScript](https://aws.amazon.com/de/sdk-for-browser/). This example shows, how to call a DynamoDB based in a input text. Therefore, HTML is combined with CSS and Javascript. The authentification is done by a functional user. This [Lambda](https://github.com/Zirkonium88/AWS/blob/master/Lambda/LoadData/handler.py) shows how to put data into a DynamoDB.

````html
<html>

<!-- Define the styles with CSS -->

<style>
    
    table {
        width: 100%;
        margin: 20px auto;
        table-layout: auto;
    }

    .fixed {
        table-layout: fixed;
    }

    table, td, th {
        border-collapse: collapse;
    }

    th,td {
    padding: 10px;
    border: solid 1px;
    text-align: center;
    }

</style>

<!-- Define a text input field in HTML -->

<input type="text" id="MY_ID_TEXT" value="Trainings-ID" style="color:#3C3E47;">

<!-- Define a button which calls callDynamo()-->
<a onclick="callDynamo();" title="Enter">Enter</a>

<!-- Define a dynamic HTML table whit three columns-->
<table>
    <tr>
        <th>id</th>
        <th>code</th>
        <th>data</th>
    </tr>
    <tbody id="tbody"></tbody>
</table>

<!-- Define a textarea for errors-->
<textarea readonly id= "textarea" style="width:400px; height:800px"></textarea>

<!-- Load the SDK-->
<script src="https://sdk.amazonaws.com/js/aws-sdk-2.7.16.min.js"></script>

<script>

/* Get configurations */
AWS.config.update({
  region: "eu-central-1",
  endpoint: 'dynamodb.eu-central-1.amazonaws.com',
  accessKeyId: "YOUR_ACCESS_KEY",
  secretAccessKey: "YOUR_SECRET_ACCESS_KEY"
});

/* Load DynamoDB client */
var dynamodb = new AWS.DynamoDB();
var docClient = new AWS.DynamoDB.DocumentClient();
/* Define callDynamo() */

function callDynamo() {

    /* Get MY_ID_TEXT from HTML input */
    var x = document.getElementById("MY_ID_TEXT").value;

    /* Eraise existing table */
    document.getElementById('tbody').innerHTML = "";

    /* Define the DynmoDB call. Get all items with primary key MY_ID_TEXT */
    var params = {
        TableName : "SAMPLE_TABLE",
        KeyConditionExpression: "#id = :id",
        ExpressionAttributeNames:{
            "#id": "id"
        },
        ExpressionAttributeValues: {
            ":id": x
        }
    };

    docClient.query(params, function(err, data) {
        if (err) {

            /* Display error message */
            document.getElementById('textarea').innerHTML += "Unable to query. Error: " + "\n" + JSON.stringify(err, undefined, 2);
        } else {

            /* Return results to the HTML table*/
            data.Items.forEach(function(trccodes) {
                document.getElementById('tbody').innerHTML += "<tr>" + "<td>" + trccodes.training + "</td>" + "<td>" + trccodes.id + "</td>" + "<td>" + trccodes.code  + "</td>" + "</tr>";
            });

        }
    })
}

</script>

</html>

````