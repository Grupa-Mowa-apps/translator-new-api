# AWS AI Practitioner - Lista Narzędzi

## 🤖 SERWISY AI/ML

### **Amazon SageMaker**
- **Cel:** Kompleksowa platforma do budowania, trenowania i wdrażania modeli ML
- **Funkcje:** Training jobs, endpoints, notebooks, autopilot
- **Kiedy używać:** Gdy budujesz własne modele ML od zera

### **Amazon Bedrock**
- **Cel:** Dostęp do gotowych modeli foundation (LLM) przez API
- **Funkcje:** Claude, Llama, Stable Diffusion - bez zarządzania infrastrukturą
- **Kiedy używać:** Gdy chcesz używać gotowych modeli AI (ChatGPT-like)

### **Amazon Q**
- **Cel:** Asystent AI dla biznesu i deweloperów
- **Funkcje:** Odpowiedzi na pytania, generowanie kodu, analiza dokumentów
- **Kiedy używać:** Chatbot dla pracowników, pomoc w kodowaniu

---

## 👁️ COMPUTER VISION (Obrazy/Wideo)

### **Amazon Rekognition**
- **Cel:** Analiza obrazów i wideo
- **Funkcje:** Rozpoznawanie twarzy, obiektów, tekstu, moderacja treści
- **Przykład:** Wykrywanie nieodpowiednich zdjęć, rozpoznawanie celebrytów

### **Amazon Textract**
- **Cel:** Ekstrakcja tekstu i danych z dokumentów (OCR++)
- **Funkcje:** Odczytywanie faktur, formularzy, tabel z PDF/obrazów
- **Przykład:** Automatyczne przetwarzanie faktur, skanowanie dokumentów

---

## 🗣️ NATURAL LANGUAGE PROCESSING (Tekst/Mowa)

### **Amazon Comprehend**
- **Cel:** Analiza tekstu i wydobywanie informacji
- **Funkcje:** Sentiment analysis, wykrywanie języka, entity recognition
- **Przykład:** Analiza opinii klientów, klasyfikacja dokumentów

### **Amazon Translate**
- **Cel:** Tłumaczenie maszynowe
- **Funkcje:** Tłumaczenie tekstu między 75+ językami
- **Przykład:** Tłumaczenie strony www, dokumentów

### **Amazon Transcribe**
- **Cel:** Konwersja mowy na tekst (Speech-to-Text)
- **Funkcje:** Transkrypcja audio/wideo, rozpoznawanie mówców
- **Przykład:** Napisy do filmów, transkrypcja spotkań

### **Amazon Polly**
- **Cel:** Konwersja tekstu na mowę (Text-to-Speech)
- **Funkcje:** Generowanie naturalnie brzmiącej mowy
- **Przykład:** Audiobooki, asystenci głosowi, IVR

### **Amazon Lex**
- **Cel:** Budowanie chatbotów i interfejsów konwersacyjnych
- **Funkcje:** NLU (rozumienie języka), zarządzanie dialogiem
- **Przykład:** Chatbot obsługi klienta, asystent głosowy

---

## 🔮 PERSONALIZACJA I REKOMENDACJE

### **Amazon Personalize**
- **Cel:** System rekomendacji oparty na ML
- **Funkcje:** Personalizowane rekomendacje produktów, treści
- **Przykład:** "Klienci którzy kupili X, kupili też Y"

### **Amazon Forecast**
- **Cel:** Prognozowanie szeregów czasowych
- **Funkcje:** Przewidywanie popytu, sprzedaży, ruchu
- **Przykład:** Prognoza sprzedaży na następny kwartał

---

## 🔍 WYKRYWANIE ANOMALII I OSZUSTW

### **Amazon Fraud Detector**
- **Cel:** Wykrywanie oszustw online
- **Funkcje:** Detekcja fałszywych kont, transakcji, recenzji
- **Przykład:** Blokowanie podejrzanych płatności kartą

### **Amazon Lookout for Metrics**
- **Cel:** Automatyczne wykrywanie anomalii w metrykach biznesowych
- **Funkcje:** Monitorowanie KPI, alertowanie o odchyleniach
- **Przykład:** Wykrywanie spadku sprzedaży, wzrostu błędów

### **Amazon Lookout for Vision**
- **Cel:** Wykrywanie defektów w produkcji (computer vision)
- **Funkcje:** Kontrola jakości produktów na taśmie produkcyjnej
- **Przykład:** Wykrywanie uszkodzonych części w fabryce

### **Amazon Lookout for Equipment**
- **Cel:** Predykcyjna konserwacja maszyn przemysłowych
- **Funkcje:** Wykrywanie anomalii w danych z czujników
- **Przykład:** Przewidywanie awarii maszyn przed ich wystąpieniem

---

## 📊 DANE I ETL

### **AWS Glue**
- **Cel:** Serverless ETL (Extract, Transform, Load)
- **Funkcje:** Przygotowanie danych, crawlers, Data Catalog
- **Kiedy używać:** Czyszczenie i transformacja danych przed ML

### **AWS Glue Data Catalog**
- **Cel:** Centralny katalog metadanych
- **Funkcje:** Przechowywanie informacji o strukturze, lokalizacji danych
- **Kiedy używać:** Zarządzanie metadanymi dla Athena, Redshift, EMR

### **Amazon Athena**
- **Cel:** Zapytania SQL bezpośrednio na danych w S3
- **Funkcje:** Serverless, płacisz za zapytanie
- **Kiedy używać:** Analiza danych bez ładowania do bazy

### **Amazon S3 (Simple Storage Service)**
- **Cel:** Przechowywanie obiektów (plików)
- **Funkcje:** Data lake, storage dla modeli ML, datasety
- **Kiedy używać:** Przechowywanie danych treningowych, modeli

### **Amazon Kinesis**
- **Cel:** Przetwarzanie danych strumieniowych w czasie rzeczywistym
- **Funkcje:** Kinesis Data Streams, Firehose, Analytics
- **Kiedy używać:** Real-time analytics, streaming data

---

## 🔐 BEZPIECZEŃSTWO I ZGODNOŚĆ

### **Amazon Macie**
- **Cel:** Wykrywanie i ochrona wrażliwych danych (PII)
- **Funkcje:** Skanowanie S3 w poszukiwaniu danych osobowych
- **Przykład:** Znajdowanie numerów kart kredytowych w plikach

### **AWS IAM (Identity and Access Management)**
- **Cel:** Zarządzanie dostępem do zasobów AWS
- **Funkcje:** Users, roles, policies, permissions
- **Kiedy używać:** Kontrola kto ma dostęp do modeli ML

### **Amazon GuardDuty**
- **Cel:** Wykrywanie zagrożeń bezpieczeństwa
- **Funkcje:** Monitorowanie podejrzanej aktywności w AWS
- **Przykład:** Wykrywanie nieautoryzowanego dostępu

---

## 💻 COMPUTE I INFRASTRUKTURA

### **AWS Lambda**
- **Cel:** Serverless compute - uruchamianie kodu bez serwerów
- **Funkcje:** Płacisz tylko za czas wykonania
- **Kiedy używać:** Inference dla małych modeli, event-driven ML

### **Amazon EC2 (Elastic Compute Cloud)**
- **Cel:** Wirtualne serwery w chmurze
- **Funkcje:** Różne typy instancji (CPU, GPU, pamięć)
- **Kiedy używać:** Trenowanie modeli, custom infrastructure

### **Amazon ECS/EKS**
- **Cel:** Uruchamianie kontenerów Docker
- **Funkcje:** ECS (AWS), EKS (Kubernetes)
- **Kiedy używać:** Wdrażanie modeli w kontenerach

---

## 📈 MONITORING I OPTYMALIZACJA

### **Amazon CloudWatch**
- **Cel:** Monitoring i logowanie
- **Funkcje:** Metryki, logi, alarmy, dashboardy
- **Kiedy używać:** Monitorowanie wydajności modeli, alertowanie

### **AWS CloudTrail**
- **Cel:** Audyt i śledzenie działań w AWS
- **Funkcje:** Logowanie wszystkich API calls
- **Kiedy używać:** Compliance, security audits

---

## 🎯 BUSINESS INTELLIGENCE

### **Amazon QuickSight**
- **Cel:** Business Intelligence i wizualizacja danych
- **Funkcje:** Dashboardy, raporty, ML insights
- **Kiedy używać:** Tworzenie raportów biznesowych z danych ML

---

## 🏗️ INNE WAŻNE SERWISY

### **AWS Step Functions**
- **Cel:** Orkiestracja workflow (przepływów pracy)
- **Funkcje:** Koordynacja wielu serwisów AWS
- **Kiedy używać:** Złożone pipeline ML (data prep → training → deploy)

### **Amazon EventBridge**
- **Cel:** Event bus - routing zdarzeń między serwisami
- **Funkcje:** Trigger Lambda, Step Functions na podstawie eventów
- **Kiedy używać:** Event-driven architecture dla ML

### **Amazon SNS (Simple Notification Service)**
- **Cel:** Wysyłanie powiadomień (pub/sub)
- **Funkcje:** Email, SMS, push notifications
- **Kiedy używać:** Alertowanie o wynikach modelu, anomaliach

### **Amazon SQS (Simple Queue Service)**
- **Cel:** Kolejki wiadomości
- **Funkcje:** Asynchroniczne przetwarzanie
- **Kiedy używać:** Buforowanie requestów do modelu ML

---

## 📚 KLUCZOWE KONCEPCJE DO ZAPAMIĘTANIA

### **Serverless vs Managed vs Self-Managed**
- **Serverless:** Lambda, Athena - zero zarządzania infrastrukturą
- **Managed:** SageMaker, Rekognition - AWS zarządza, Ty konfigurujesz
- **Self-Managed:** EC2 - pełna kontrola, pełna odpowiedzialność

### **Real-time vs Batch Inference**
- **Real-time:** Endpoint SageMaker, Lambda - natychmiastowa odpowiedź
- **Batch:** Batch Transform, Glue - przetwarzanie dużych zbiorów

### **Training vs Inference**
- **Training:** Tworzenie modelu (SageMaker Training Jobs)
- **Inference:** Używanie modelu (SageMaker Endpoints, Lambda)

---

## 🎓 TIPS DO EGZAMINU

1. **Rozpoznaj use case** - każdy serwis ma swoje zastosowanie
2. **Serverless first** - AWS preferuje rozwiązania serverless
3. **Managed services** - używaj gotowych serwisów zamiast budować od zera
4. **Cost optimization** - batch vs real-time, reserved instances
5. **Security** - IAM, encryption, VPC
6. **Scalability** - auto-scaling, distributed training

---

## 📖 NAJCZĘSTSZE PYTANIA NA EGZAMINIE

- **Kiedy użyć SageMaker vs Bedrock?** Custom model vs gotowy LLM
- **Kiedy użyć Lambda vs SageMaker Endpoint?** Mały model/niski ruch vs duży model/wysoki ruch
- **Kiedy użyć Rekognition vs własny model?** Standardowe zadania vs specjalistyczne
- **Co to jest Data Catalog?** Metadata repository dla Glue/Athena
- **Batch vs Real-time inference?** Nie potrzebujesz natychmiastowej odpowiedzi vs potrzebujesz
- **Overfitting?** Za mało danych lub za skomplikowany model
- **Model interpretability?** Jak łatwo wyjaśnić decyzje modelu

---

**Powodzenia na egzaminie! 🚀**
