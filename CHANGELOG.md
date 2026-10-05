# Changelog

All notable changes to **NetSonar** are documented in this file.

The project follows a simplified version of [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-10-06

### 🎉 Initial Release

First complete portfolio release of **NetSonar — Network Traffic Sonification & Security Monitor**.

### 📡 Network Capture

* Added live packet capture using **Scapy**.
* Added Linux network interface monitoring.
* Added IPv4 packet processing.
* Added TCP, UDP, and ICMP traffic identification.
* Added source and destination IP tracking.
* Added source and destination port tracking.
* Added packet-size tracking.

### 🔍 Traffic Analysis

* Added real-time packet counting.
* Added total byte tracking.
* Added packets-per-second calculation.
* Added unique source IP statistics.
* Added unique destination IP statistics.
* Added protocol activity statistics.
* Added destination-port statistics.
* Added live statistics export to JSON.

### 🧩 Protocol Classification

Added application/service identification for common network protocols:

* HTTP
* HTTPS
* DNS
* DNS over TCP
* SSH
* FTP
* FTP-DATA
* SMTP
* POP3
* IMAP
* SMB
* RDP
* DHCP
* NTP
* SNMP
* IKE
* SSDP

### 🚨 Security Detection

Added lightweight behavioral anomaly detection.

#### Traffic Spike Detection

* Added sliding-window traffic monitoring.
* Added configurable packet-rate threshold.
* Added high-severity traffic spike alerts.

#### TCP SYN Port-Scan Detection

* Added TCP SYN activity tracking.
* Added unique destination-port analysis.
* Added configurable port-scan threshold.
* Added high-severity port-scan alerts.

### 📝 Security Event Logging

* Added persistent security event logging.
* Added timestamps to security events.
* Added event type and severity fields.
* Added source IP information for relevant detections.
* Added detected port-count information.
* Added packet-count information for traffic-spike events.

### 🔊 Network Sonification

Added the NetSonar audio intelligence engine.

* Added protocol-specific audio frequencies.
* Added packet-size-based frequency adjustment.
* Added packet-size-based volume adjustment.
* Added packet-size-based duration adjustment.
* Added Linux ALSA/`aplay` audio playback.
* Added generated WAV tone caching.
* Added dedicated security alert tones.
* Added audio telemetry export.

### 〰️ Audio Waveform Visualization

* Added live audio-event telemetry.
* Added JSON-based audio event storage.
* Added dynamic waveform reconstruction.
* Added frequency visualization.
* Added audio event tracking.
* Added latest sound-event information.

### 📊 SOC Dashboard

Added a Streamlit-based security monitoring dashboard.

Dashboard includes:

* Live monitoring status
* Network interface status
* Packet capture status
* Audio telemetry status
* Security event status
* Total packet metrics
* Traffic volume
* Packets-per-second statistics
* Unique source statistics
* Audio waveform visualization
* Latest sound event
* Protocol analytics
* Destination-port analytics
* Security operations metrics
* Recent security events
* Raw security logs
* Network snapshot
* Automatic dashboard refresh

### 🧪 Testing

Added automated testing using **pytest**.

Test coverage includes:

* Protocol classification
* HTTPS identification
* HTTP identification
* SSH identification
* DNS identification
* ICMP handling
* Packet counting
* Byte counting
* Protocol statistics
* Traffic spike detection
* TCP SYN port-scan detection
* Normal traffic behavior

### 🛠️ Project Infrastructure

* Added Python package initialization files.
* Added `pytest.ini`.
* Added project `.gitignore`.
* Added dependency management through `requirements.txt`.
* Added project configuration directory.
* Added runtime data directories.
* Added runtime log directory.
* Added MIT License.
* Added comprehensive project documentation.

### 🔐 Security & Privacy

* Runtime telemetry files are excluded from Git.
* Runtime security logs are excluded from Git.
* Local TLS configuration workaround is excluded from Git.
* Environment and secret files are exclu
