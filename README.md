# Quiz Test Platform (Intellektual Quiz Arena)

Django asosida yaratilgan interaktiv savollar platformasi. Unda 16 ta maxfiy raqamlangan kartochkalar bo'lib, har bir savol tanlanganda ochiladi va qayta tanlash imkoniyati bloklanadi.

## Xususiyatlari

- **Django loyihasi va `quiz` ilovasi**: To'liq sozlangan va integratsiya qilingan.
- **Superadmin hisobi**:
  - **Login**: `sevinch`
  - **Parol**: `123`
- **Savollar bazasi**: `questions.json` faylidagi barcha 16 ta savol yuklangan.
- **Premium Dizayn (UI/UX)**:
  - Tailwind CSS, Google Fonts (*Outfit* va *Plus Jakarta Sans*) va FontAwesome ikonkalari.
  - 3D kartochkalar, zamonaviy glassmorphism va animatsiyalar.
  - O'rnatilgan Web Audio API effektlari (savol ochilganda akkord ovozi va tugmalar bosilishi).
- **Interaktiv Quiz Mexanizmi va Random Savollar**:
  - Dastlab faqat 16 ta raqam (1 dan 16 gacha) usti yopiq holda ko'rinadi.
  - Kartochkalar ortidagi savollar har bir o'yinda **tasodifiy (random)** tartibda joylashtiriladi.
  - Kartochka bosilganda silliq animatsiya bilan savol ochiladi va modal darchada ko'rsatiladi.
  - Vaqt o'lchagich (taymer) integratsiya qilingan.
  - Ochilgan savol darhol qulflanadi va qayta tanlab bo'lmaydi.
  - Holat ma'lumotlar bazasida (`GameCard` modeli) saqlanadi, sahifa yangilansa ham saqlanib qoladi.
  - **Qayta boshlash (Reset)** bosilganda barcha savollar avtomatik ravishda **tasodifiy (random) tarzda qayta aralashtiriladi** va doska yangilanadi.

---

## Ishga tushirish (Qo'llanma)

1. **Virtual muhitni faollashtirish**:
   ```bash
   source /home/shokhjahon/startapp/quiz-test/venv/bin/activate
   ```

2. **Serverni ishga tushirish**:
   ```bash
   python manage.py runserver 8000
   ```

3. **Brauzerda ochish**:
   - Asosiy sahifa va Login: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
   - Superadmin ma'lumotlari:
     - Login: `sevinch`
     - Parol: `123`
   - Django Admin paneli: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Foydali buyruqlar

- Savollarni `questions.json` faylidan qayta yuklash:
  ```bash
  python manage.py load_questions
  ```
- Superadminni qayta sozlash:
  ```bash
  python manage.py setup_admin
  ```
- Testlarni ishga tushirish:
  ```bash
  python manage.py test
  ```