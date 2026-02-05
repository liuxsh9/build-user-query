# Domain Tag Research & Curation

## Emerging Technology Domains

### 1. MLOps (Machine Learning Operations)
- **Ecosystem**: MLflow, Kubeflow, Weights & Biases, Neptune.ai
- **Distinct from ML**: Focuses on deployment, monitoring, versioning of ML models
- **Job market**: Strong demand for MLOps engineers
- **Validation**: ✅ Passes all tests (scope, granularity, distinctiveness, ecosystem)

### 2. DataOps
- **Ecosystem**: Apache Airflow, dbt, Great Expectations, Prefect
- **Distinct from Data Science**: Focuses on data pipeline automation and quality
- **Job market**: Growing field with dedicated roles
- **Validation**: ✅ Passes all tests

### 3. Edge Computing
- **Ecosystem**: AWS IoT Greengrass, Azure IoT Edge, K3s, EdgeX Foundry
- **Distinct from IoT**: Focuses on computation at network edge, not just devices
- **Job market**: Growing with 5G and IoT expansion
- **Validation**: ✅ Passes all tests

### 4. Serverless Computing
- **Ecosystem**: AWS Lambda, Azure Functions, Google Cloud Functions, Serverless Framework
- **Distinct from Cloud**: Specific architectural pattern with FaaS
- **Job market**: Mainstream adoption, dedicated roles
- **Validation**: ✅ Passes all tests

### 5. Platform Engineering
- **Ecosystem**: Backstage, Crossplane, Port, Humanitec
- **Distinct from DevOps**: Focuses on internal developer platforms
- **Job market**: Rapidly growing field with dedicated teams
- **Validation**: ✅ Passes all tests

### 6. Site Reliability Engineering (SRE)
- **Ecosystem**: Prometheus, Grafana, PagerDuty, Datadog
- **Distinct from DevOps**: Specific discipline with SLOs, error budgets
- **Job market**: Well-established with dedicated SRE roles
- **Validation**: ✅ Passes all tests

### 7. FinOps (Cloud Financial Operations)
- **Ecosystem**: CloudHealth, Kubecost, Infracost, Vantage
- **Distinct from DevOps**: Focuses on cloud cost optimization
- **Job market**: Growing with cloud adoption
- **Validation**: ✅ Passes all tests

### 8. Low-Code/No-Code Development
- **Ecosystem**: OutSystems, Mendix, Bubble, Retool
- **Distinct from traditional dev**: Specific paradigm with visual builders
- **Job market**: Growing segment, citizen developers
- **Validation**: ⚠️ Borderline - may be too broad, but has distinct ecosystem
- **Decision**: INCLUDE - has established ecosystem and job market

## Specialized Application Subfields

### 9. Bioinformatics
- **Ecosystem**: BioPython, Bioconductor, Galaxy, BLAST
- **Distinct**: Unique algorithms, data formats (FASTA, BAM), domain expertise
- **Job market**: Specialized field with dedicated roles
- **Validation**: ✅ Passes all tests

### 10. Geospatial/GIS
- **Ecosystem**: QGIS, PostGIS, Leaflet, Mapbox, GDAL
- **Distinct**: Spatial data structures, coordinate systems, mapping
- **Job market**: Established field with GIS specialists
- **Validation**: ✅ Passes all tests

### 11. Audio Processing
- **Ecosystem**: JUCE, PortAudio, Web Audio API, Superpowered
- **Distinct**: Signal processing, codecs, real-time constraints
- **Job market**: Music tech, podcasting, voice applications
- **Validation**: ✅ Passes all tests

### 12. Video Processing
- **Ecosystem**: FFmpeg, OpenCV, GStreamer, WebRTC
- **Distinct**: Video codecs, streaming, transcoding
- **Job market**: Streaming platforms, video editing, surveillance
- **Validation**: ⚠️ May overlap with Computer Vision
- **Decision**: INCLUDE - distinct from CV (focuses on encoding/streaming, not analysis)

### 13. Quantum Computing
- **Ecosystem**: Qiskit, Cirq, Q#, PennyLane
- **Distinct**: Quantum algorithms, qubits, quantum gates
- **Job market**: Emerging but growing with IBM, Google, AWS investments
- **Validation**: ✅ Passes all tests

### 14. Augmented Reality (AR)
- **Ecosystem**: ARKit, ARCore, Vuforia, Unity AR
- **Distinct**: Spatial computing, marker tracking, SLAM
- **Job market**: Growing with Apple Vision Pro, Meta Quest
- **Validation**: ✅ Passes all tests

### 15. Virtual Reality (VR)
- **Ecosystem**: Unity VR, Unreal VR, WebXR, OpenVR
- **Distinct**: Immersive 3D, motion tracking, VR interactions
- **Job market**: Gaming, training, simulation
- **Validation**: ✅ Passes all tests

### 16. Computer Graphics
- **Ecosystem**: OpenGL, Vulkan, DirectX, Three.js, Blender API
- **Distinct**: Rendering, shaders, 3D math, graphics pipelines
- **Job market**: Gaming, visualization, CAD
- **Validation**: ⚠️ May overlap with Game Development
- **Decision**: INCLUDE - broader than games (CAD, visualization, scientific)

### 17. Simulation
- **Ecosystem**: Gazebo, CARLA, AirSim, Unity Simulation
- **Distinct**: Physics engines, environment modeling, synthetic data
- **Job market**: Robotics, autonomous vehicles, training
- **Validation**: ✅ Passes all tests

## Cross-Cutting Domains

### 18. Accessibility (a11y)
- **Ecosystem**: NVDA, JAWS, axe, WAVE, ARIA
- **Distinct**: WCAG standards, screen readers, assistive tech
- **Job market**: Growing focus on inclusive design
- **Validation**: ✅ Passes all tests

### 19. Internationalization (i18n)
- **Ecosystem**: ICU, gettext, i18next, FormatJS
- **Distinct**: Localization, Unicode, RTL, pluralization
- **Job market**: Global products require i18n expertise
- **Validation**: ✅ Passes all tests

### 20. Real-time Systems
- **Ecosystem**: FreeRTOS, Zephyr, VxWorks, RT-Linux
- **Distinct**: Hard/soft real-time constraints, deterministic behavior
- **Job market**: Embedded, automotive, industrial control
- **Validation**: ✅ Passes all tests

### 21. Observability
- **Ecosystem**: OpenTelemetry, Jaeger, Zipkin, Honeycomb
- **Distinct**: Traces, metrics, logs (three pillars), distributed tracing
- **Job market**: Modern cloud-native focus
- **Validation**: ⚠️ May overlap with Monitoring
- **Decision**: INCLUDE - distinct focus on distributed systems and tracing

### 22. Monitoring
- **Ecosystem**: Prometheus, Grafana, Nagios, Zabbix
- **Distinct**: Metrics collection, alerting, dashboards
- **Job market**: Established field
- **Validation**: ⚠️ May overlap with Observability and SRE
- **Decision**: EXCLUDE - too much overlap with Observability and SRE

### 23. Logging
- **Ecosystem**: ELK Stack, Splunk, Fluentd, Loki
- **Distinct**: Log aggregation, parsing, search
- **Job market**: Part of observability stack
- **Validation**: ⚠️ Too narrow, part of Observability
- **Decision**: EXCLUDE - covered by Observability

### 24. Performance Engineering
- **Ecosystem**: JMeter, Gatling, k6, Locust
- **Distinct**: Load testing, profiling, optimization
- **Job market**: Specialized performance engineers
- **Validation**: ✅ Passes all tests

### 25. Compliance/Regulatory
- **Ecosystem**: GDPR tools, HIPAA compliance, SOC 2, PCI DSS
- **Distinct**: Legal requirements, audit trails, data governance
- **Job market**: Growing with data privacy regulations
- **Validation**: ✅ Passes all tests

## Additional Candidates (from research)

### 26. Data Engineering
- **Ecosystem**: Spark, Kafka, Flink, Snowflake
- **Distinct from Data Science**: Focuses on data pipelines, not analysis
- **Job market**: Huge demand for data engineers
- **Validation**: ✅ Passes all tests
- **Decision**: INCLUDE - distinct from existing Data Science domain

### 27. Search Engineering
- **Ecosystem**: Elasticsearch, Solr, Algolia, Meilisearch
- **Distinct**: Full-text search, relevance tuning, indexing
- **Job market**: Specialized search engineers
- **Validation**: ✅ Passes all tests

## Final Curated List (22 new domains)

**Emerging Technology (8):**
1. MLOps
2. DataOps  
3. Edge Computing
4. Serverless Computing
5. Platform Engineering
6. Site Reliability Engineering
7. FinOps
8. Low-Code/No-Code Development

**Specialized Subfields (10):**
9. Bioinformatics
10. Geospatial/GIS
11. Audio Processing
12. Video Processing
13. Quantum Computing
14. Augmented Reality
15. Virtual Reality
16. Computer Graphics
17. Simulation
18. Data Engineering

**Cross-Cutting (4):**
19. Accessibility
20. Internationalization
21. Real-time Systems
22. Observability
23. Performance Engineering
24. Compliance/Regulatory
25. Search Engineering

**Total: 32 existing + 25 new = 57 domains**

**Excluded:**
- Monitoring (overlaps with Observability/SRE)
- Logging (part of Observability)
