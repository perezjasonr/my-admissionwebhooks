from flask import Flask, request, jsonify

admission_controller = Flask(__name__)


@admission_controller.route('/validate/deployments', methods=['POST'])
def deployment_webhook():
    request_info = request.get_json()
    uid = request_info["request"]["uid"]
    if request_info["request"]["object"]["metadata"]["labels"].get("allow"):
        return admission_response(True, "Allow label exists", uid)
    return admission_response(False, "Not allowed without allow label", uid)


def admission_response(allowed, message, uid):
    return jsonify(
        {
            "apiVersion": "admission.k8s.io/v1",
            "kind": "AdmissionReview",
            "response": {
                "allowed": allowed,
                "uid": uid,
                "status": {
                    "message": message
                }
            }
        }
    )


if __name__ == '__main__':
    admission_controller.run(host='0.0.0.0', port=443,
                             ssl_context=("/certs/tls.crt", "/certs/tls.key"))
