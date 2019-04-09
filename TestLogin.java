package com.example.javatest;

import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertNotNull;

public class TestLogin {

    static WebDriver driver;
    final String ProfUserName = "professor";
    final String PASSWORD = "sutd1234";

    final String StudentUserName = "student";
    final String BRUTEPASSWORD = "1111111111";

//    In this class, we test the following:
//    - Login as a Professor and goes to submit course details page
//    - Login with wrong details (wrong password & correct username,
// wrong username & correct password, wrong username & password) followed by correct details
//    - Brute-force login (with 6 attempts), wait for 3 minutes lockout period, before logging in with correct details



    @BeforeClass
    public static void setup() {
        System.setProperty("webdriver.gecko.driver", "C:\\Users\\It'sMine\\AndroidStudioProjects\\JavaTest\\Javatest\\libs\\geckodriver.exe");
        driver = new FirefoxDriver();
    }

    @After
    public void logout() {
        driver.get("http://127.0.0.1:8000");
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));

        // find Log out button
        WebElement logoutButton = null;
        for (WebElement link : links) {
            if (link.getText().equals("Log out")) {
                logoutButton = link;
            }
        }

        if (logoutButton != null) logoutButton.click();

    }

    @Test
    public void test_login_to_submit_course_details() {
        driver.get("http://127.0.0.1:8000");
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));

        // find Log in button
        WebElement loginButton = null;
        for (WebElement link : links) {
            if (link.getText().equals("Log in")) {
                loginButton = link;
            }
        }

        if (loginButton != null) {
            loginButton.click();
        }

        WebElement username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(ProfUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/professors/", actualURL);

        // clicks dropdown and goes to submit course details
        WebElement dropdown = driver.findElement(By.id("navbarDropdown"));
        dropdown.click();

        java.util.List<WebElement> dropdownItems = driver.findElements(By.className("dropdown-item"));
        WebElement submitCourse = null;
        for (WebElement item : dropdownItems) {
            if (item.getText().equals("Submit Course Details")) {
                submitCourse = item;
                break;
            }
        }

        if (submitCourse != null) submitCourse.click();

        // checks if we are in submit course page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/professors/submitdetails", actualURL);
    }

    @Test
    public void test_login_with_wrong() {
        driver.get("http://127.0.0.1:8000");
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));

        // find Log in button
        WebElement loginButton = null;
        for (WebElement link : links) {
            if (link.getText().equals("Log in")) {
                loginButton = link;
            }
        }

        if (loginButton != null) {
            loginButton.click();
        }

        WebElement username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys("");

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are still in the same page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/accounts/login/", actualURL);

        username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(ProfUserName);

        password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys("");

        LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are still in the same page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/accounts/login/", actualURL);

        username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(ProfUserName);

        password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are still in the same page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/professors/", actualURL);

    }

    @Test
    public void test_login_brute_force() throws InterruptedException {
        driver.get("http://127.0.0.1:8000");
        java.util.List<WebElement> links = driver.findElements(By.tagName("a"));

        // find Log in button
        WebElement loginButton = null;
        for (WebElement link : links) {
            if (link.getText().equals("Log in")) {
                loginButton = link;
            }
        }

        if (loginButton != null) {
            loginButton.click();
        }

        WebElement username = null;
        WebElement password = null;
        WebElement LoginButton = null;

        // brute-force for 6 times
        for (int i = 0; i < 6; i++) {
            username = driver.findElement(By.id("id_username"));
            username.clear();
            username.sendKeys(StudentUserName);

            password = driver.findElement(By.id("id_password"));
            password.clear();
            password.sendKeys(BRUTEPASSWORD);

            LoginButton = driver.findElement(By.id("id_login"));
            LoginButton.click();

            // checks that we are still in the same page
            String actualURL = driver.getCurrentUrl();
            assertNotNull(actualURL);
            assertEquals("http://127.0.0.1:8000/accounts/login/", actualURL);

        }

        // key in the correct username & password
        username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(StudentUserName);

        password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are still in the same page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/accounts/login/", actualURL);

        // wait for lockout period
        Thread.sleep(3020);

        // key in the correct username & password
        username = driver.findElement(By.id("id_username"));
        username.clear();
        username.sendKeys(StudentUserName);

        password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks that we are finally logged in
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/students/", actualURL);


    }
}
