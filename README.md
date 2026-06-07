# Discord Ticket Bot 🎫

Discord sunucunuz için profesyonel ticket sistemi.

## Özellikler

✅ Ticket açma butonu  
✅ Otomatik kanal oluşturma  
✅ Yetkili erişimi  
✅ Otomatik kanal silme  
✅ Kullanıcı dostu arayüz  

## Kurulum

### 1. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 2. .env Dosyası Oluşturun

```env
DISCORD_TOKEN=your_bot_token_here
```

**Bot token'ı nasıl alınır:**
1. [Discord Developer Portal](https://discord.com/developers/applications) açın
2. Uygulamanızı seçin
3. "Bot" bölümüne gidin
4. "Reset Token" butonuna tıklayın
5. Token'ı kopyalayın ve `.env` dosyasına yapıştırın

### 3. Botu Çalıştırın

```bash
python ticket_bot.py
```

## Kullanım

### Admin Komutları

1. **Ticket Sistemini Kurma:**
   ```
   !ticket_setup
   ```
   Bu komut ticket sistemi mesajını oluşturur ve "Ticket Aç" butonunu ekler.

### Bot Özellikleri

- **Ticket Açma**: "Ticket Aç" butonuna tıklayarak yeni ticket oluşturun
- **Kullanıcı Dostu**: Her kullanıcı sadece 1 aktif ticket açabilir
- **Güvenli**: Sadece ticket açan kullanıcı ve yetkililer kanalı görebilir
- **Otomatik Silme**: Ticket kapatıldıktan 5 saniye sonra kanal otomatik silinir

## Rol Yapılandırması

Bot aşağıdaki rolleri otomatik olarak tanır:
- **Admin** - Tam erişim
- **Support** - Destek erişimi

Kendi rollerinize göre `ticket_bot.py` dosyasında değişiklik yapabilirsiniz:

```python
admin_role = discord.utils.get(guild.roles, name="Moderator")  # "Admin" yerine "Moderator"
support_role = discord.utils.get(guild.roles, name="Helper")    # "Support" yerine "Helper"
```

## Bot İzinleri

Botun şu izinlere ihtiyacı vardır:
- ✅ Kanalları yönet
- ✅ Mesaj gönder
- ✅ Mesajları okuma
- ✅ Rol yönet
- ✅ Üyeleri yönet

**Davet linki oluştururken:**
1. Discord Developer Portal → OAuth2 → URL Generator
2. Scopes: `bot`
3. Permissions: `Administrator` (kolay) veya yukarıdaki izinleri seçin

## Sorun Giderme

**Bot yanıt vermiyor?**
- TOKEN'ı kontrol edin (.env dosyasında)
- Bot'u sunucunuza davet ettiğinizden emin olun
- Bot'un yeterli izinleri olup olmadığını kontrol edin

**Kanal silinmiyor?**
- Bot rolüne kanal silme izni verin
- Bot rolünün sunucu rollerinin üstünde olduğundan emin olun

**Hata: "Bot token is invalid"**
- Token'ı yenileyin (Developer Portal'den)
- .env dosyasında doğru yere yapıştırıldığından emin olun

## Dosya Yapısı

```
discord-ticket-bot/
├── ticket_bot.py       # Ana bot dosyası
├── .env                # Ortam değişkenleri
├── requirements.txt    # Python bağımlılıkları
└── README.md          # Bu dosya
```

## Lisans

MIT License