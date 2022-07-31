#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = YOUR_SSID_NAME
const char* password = YOUS_WIFI_PASSWORD

// Find this awsEndpoint in the AWS Console: Manage - Things, choose your thing
// choose Interact, its the HTTPS Rest endpoint 
const char* awsEndpoint = XXXX

// For the two certificate strings below paste in the text of your AWS 
// device certificate and private key:
#define Relay1 15
#define Relay2 2
#define Relay3 4

// xxxxxxxxxx-certificate.pem.crt
static const char certificatePemCrt[] PROGMEM = R"EOF(
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
)EOF";

// xxxxxxxxxx-private.pem.key
static const char privatePemKey[] PROGMEM = R"EOF(
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
)EOF";

// This is the AWS IoT CA Certificate from: 
// https://docs.aws.amazon.com/iot/latest/developerguide/managing-device-certs.html#server-authentication
// This one in here is the 'RSA 2048 bit key: Amazon Root CA 1' which is valid 
// until January 16, 2038 so unless it gets revoked you can leave this as is:
static const char caPemCrt[] PROGMEM = R"EOF(
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
)EOF";

BearSSL::X509List client_crt(certificatePemCrt);
BearSSL::PrivateKey client_key(privatePemKey);
BearSSL::X509List rootCert(caPemCrt);

WiFiClientSecure wiFiClient;
void msgReceived(char* topic, byte* payload, unsigned int len);
PubSubClient pubSubClient(awsEndpoint, 8883, msgReceived, wiFiClient); 

#define AWS_IOT_PUBLISH_TOPIC   "user"

#define AWS_IOT_SUBSCRIBE_TOPIC1 "esp32/relay1"
#define AWS_IOT_SUBSCRIBE_TOPIC2 "esp32/relay2"
#define AWS_IOT_SUBSCRIBE_TOPIC3 "esp32/relay3"

void setup() {
  Serial.begin(115200); Serial.println();
  Serial.println("ESP8266 AWS IoT Example");

  Serial.print("Connecting to "); Serial.print(ssid);
  WiFi.begin(ssid, password);
  WiFi.waitForConnectResult();
  Serial.print(", WiFi connected, IP address: "); Serial.println(WiFi.localIP());
  
  // get current time, otherwise certificates are flagged as expired
  setCurrentTime();
  pinMode(Relay1, OUTPUT);
  pinMode(Relay2, OUTPUT);
  pinMode(Relay3, OUTPUT);
  
  wiFiClient.setClientRSACert(&client_crt, &client_key);
  wiFiClient.setTrustAnchors(&rootCert);
  pubSubCheckConnect();
  digitalWrite(Relay1,1);
  digitalWrite(Relay2,1);
  digitalWrite(Relay3,1);
}

unsigned long lastPublish;
int msgCount;

void loop() {

  pubSubClient.loop();
}

void msgReceived(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on "); Serial.print(topic); Serial.print(": ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  messageHandler(topic,payload,length);  
}

void pubSubCheckConnect() {
  if ( ! pubSubClient.connected()) {
    Serial.print("PubSubClient connecting to: "); Serial.print(awsEndpoint);
    while ( ! pubSubClient.connected()) {
      Serial.print(".");
      pubSubClient.connect("user");
    }
    Serial.println(" connected");
    //pubSubClient.subscribe("");
    //pubSubClient.setCallback(messageHandler);
    pubSubClient.subscribe(AWS_IOT_SUBSCRIBE_TOPIC1);
    pubSubClient.subscribe(AWS_IOT_SUBSCRIBE_TOPIC2);
    pubSubClient.subscribe(AWS_IOT_SUBSCRIBE_TOPIC3);
    }
  
}

void messageHandler(char* topic, byte* payload, unsigned int length)
{
  Serial.print("incoming: ");
  Serial.println(topic);

  if ( strstr(topic, "esp32/relay1") )
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    String Relay_data = doc["status"];
    int r = Relay_data.toInt();
    Serial.print(r);
    digitalWrite(Relay1, !r);
    Serial.print("Relay1 - "); Serial.println(Relay_data);
  }

  if ( strstr(topic, "esp32/relay2") )
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    String Relay_data = doc["status"];
    int r = Relay_data.toInt();
    digitalWrite(Relay2, !r);
    Serial.print("Relay2 - "); Serial.println(Relay_data);
  }

  if ( strstr(topic, "esp32/relay3") )
  {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);
    String Relay_data = doc["status"];
    int r = Relay_data.toInt();
    digitalWrite(Relay3, !r);
    Serial.print("Relay3 - "); Serial.println(Relay_data);
  }



}

void setCurrentTime() {
  configTime(3 * 3600, 0, "pool.ntp.org", "time.nist.gov");

  Serial.print("Waiting for NTP time sync: ");
  time_t now = time(nullptr);
  while (now < 8 * 3600 * 2) {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println("");
  struct tm timeinfo;
  gmtime_r(&now, &timeinfo);
  Serial.print("Current time: "); Serial.print(asctime(&timeinfo));
}
