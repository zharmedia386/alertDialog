# Import all library needed
from lib import *

# Set up global variables for login purposes
email = ""
password = ""
driver = None
driveStorage = 0


# STEP 1 - input email and password for drive account using pyqt5
class LoginWindow(QWidget):
   def __init__(self):
      super().__init__()

      self.UI()

   def UI(self):
      self.resize(300, 100)
      self.move(300, 300)
      self.setWindowTitle("Login Google Drive Account")

      # email attribute
      self.email_label = QLabel("Email: ", self)
      self.email_edit = QLineEdit(self)

      # password attribute
      self.password_label = QLabel("Password: ", self)
      self.password_edit = QLineEdit(self)
      self.password_edit.setEchoMode(QLineEdit.Password)
      
      # button login and cancel
      self.login_button = QPushButton("Login", self)

      # button event
      self.login_button.clicked.connect(self.login)

      # layouting 
      layout = QGridLayout()
      layout.addWidget(self.email_label, 0, 0)
      layout.addWidget(self.email_edit, 0, 1)
      layout.addWidget(self.password_label, 1, 0)
      layout.addWidget(self.password_edit, 1, 1)
      layout.addWidget(self.login_button, 2, 1, 1, 2)

      self.setLayout(layout)
      
   def login(self):
      global email, password
      email = self.email_edit.text()
      password = self.password_edit.text()
      self.close()


 # STEP 2 - Login Google Account with certain email and passwords and get the storage Drive
class ScrapeDriveStorage() :
   def __init__(self):
      # change value of driver global variable
      global driver
      driver = webdriver.Chrome('G:\ChromeDriver\chromedriver.exe')

      self.loginGoogle()
      self.getStorageDrive()

   def loginGoogle(self):
      driver.get('https://www.google.com/accounts/Login?hl=id&continue=http://www.google.co.jp/')
      driver.maximize_window()

      # get the element of input email and send_key
      time.sleep(1)
      driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(email)
      driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input").send_keys(Keys.RETURN)

      # get the element of input password and send_key
      time.sleep(1)
      passWordBox = driver.find_element_by_xpath('//*[@id ="password"]/div[1]/div / div[1]/input')
      passWordBox.send_keys(password)

      nextButton = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
      nextButton[0].click()

   def getStorageDrive(self):
      # change value of driveStorage global variable
      global driveStorage

      # Get the size of used capacity
      time.sleep(2)
      driver.get('https://drive.google.com/drive/')
      time.sleep(2)
      size_used = driver.find_element_by_xpath("//div[contains(@class, 'QdYI6c')]").text
      print(f'Scrape result : {size_used}')

      # Convert into float type
      size_used = size_used.replace(' GB digunakan', '')
      size_used = size_used.replace(',', '.')
      driveStorage = float(size_used)
      print(f'Your drive capasity is : {driveStorage} GB')



# STEP 3 - Alert Dialog when exceeding capacity

# Dialog if Exceeding Capacity
class ExceedingLimit(QWidget):
   def __init__(self):
      super().__init__()

      self.setupUi()
   
   def goToMultCloud(self) :
      driver.get('https://www.multcloud.com/')
      time.sleep(0.5)
      self.close()
      print('Go to MultCloud')

   def setupUi(self):
      # window customization
      self.resize(400, 100)
      self.move(300, 300)
      self.setWindowTitle('Overload Drive Capacity')
      
      # Create a label widget
      self.label = QLabel()
      self.label.setText('Your current size is : ' + str(driveStorage) + ' GB and exceeding the maximum limit.\n' + 'Transfer your files to others cloud platform using MultCloud now!' )
      
      # Create a button in the window
      self.linkButton = QPushButton('\t Go to MultCloud')
      self.cancelButton = QPushButton('\t Close')
      
      # Set Layout horizontally
      hbox = QHBoxLayout()
      hbox.addWidget(self.linkButton)
      hbox.addWidget(self.cancelButton)

      # set button click event
      self.linkButton.clicked.connect(self.goToMultCloud)
      self.cancelButton.clicked.connect(self.close)
      
      # Set Layout vertically
      layout = QVBoxLayout()
      layout.addWidget(self.label)
      layout.addLayout(hbox)
      self.setLayout(layout)


# Dialog if not Exceeding Capacity
class NotExceedingLimit(QWidget):
   def __init__(self):
      super().__init__()

      self.setupUi()

   def setupUi(self,):
      # window customization
      self.resize(400, 100)
      self.move(300, 300)
      self.setWindowTitle('Drive Capacity is stable')
      
      # Create a label widget
      self.label = QLabel()
      self.label.setText('Your current size is : ' + str(driveStorage) + ' GB and not exceeding the maximum limit.\n')
      
      # Create a button in the window
      self.cancelButton = QPushButton('\t Close')
      
      # Set Layout horizontally
      hbox = QHBoxLayout()
      hbox.addWidget(self.cancelButton)

      # set button click event
      self.cancelButton.clicked.connect(self.close)
      print('Your drive is not exceeding the limit')
      
      # Set Layout vertically
      layout = QVBoxLayout()
      layout.addWidget(self.label)
      layout.addLayout(hbox)
      self.setLayout(layout)


if __name__ == '__main__':
   # QApplication object
   app = QApplication(sys.argv)
   
   # login first
   login = LoginWindow()
   login.show()

   app.exec_()

   # get the storage drive
   if email != '' and password != '' :
      ScrapeDriveStorage()

   # if the size is exceeding the limit, show the message
   if driveStorage != 0 :
      if driveStorage > 4 :
         form = ExceedingLimit() # exceed limit
      else :
         form = NotExceedingLimit() # not exceed limit
      form.show()
      app.exec_()

   