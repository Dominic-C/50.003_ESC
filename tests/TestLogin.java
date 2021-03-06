package com.example.javatest;

import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.sql.Array;
import java.sql.Time;
import java.util.Arrays;
import java.util.concurrent.TimeUnit;

import static junit.framework.TestCase.assertEquals;
import static junit.framework.TestCase.assertNotNull;
import static junit.framework.TestCase.assertTrue;

public class TestLogin {

    static WebDriver driver;
    final String ProfUserName = "professor";
    final String PASSWORD = "sutd1234";

    final String PlannerUserName = "planner";
    final String CoordUserName = "coordinator";

    final String StudentUserName = "student";
    final String BRUTEPASSWORD = "1111111111";

    final String NOTCSVFILE = "C:\\Users\\It'sMine\\Desktop\\SUTD\\Term 5\\50.003  Elements of Software Construction\\Project Meeting\\notcsvfile.txt";
    final String WRONGCSVFILE = "C:\\Users\\It'sMine\\Desktop\\SUTD\\Term 5\\50.003  Elements of Software Construction\\Project Meeting\\wrongcsvfile.csv";

//    In this class, we test the following:
//    - Login as a Professor and visits all pages available to him
//    - Login as a TimeTable Planner and visits all pages available to him
//    - Login with wrong details (wrong password & correct username,
// wrong username & correct password, wrong username & password) followed by correct details
//    - Login as TimeTable Planner and test the upload function
//    - Login as a TimeTable Planner and test the phase function
//    - Login as a TimeTable Planner and test the revert function

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
    public void test_login_planner(){
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
        username.sendKeys(PlannerUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/", actualURL);

        // clicks dropdown and goes to Upload First Draft
        WebElement dropdown = driver.findElement(By.id("navbarDropdown"));
        dropdown.click();

        java.util.List<WebElement> dropdownItems = driver.findElements(By.className("dropdown-item"));
        WebElement uploaddraft = null;
        for (WebElement item : dropdownItems) {
            if (item.getText().equals("Upload First Draft")) {
                uploaddraft = item;
                break;
            }
        }

        if (uploaddraft != null) uploaddraft.click();

        // checks if we are in upload first draft page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/upload", actualURL);

        // clicks dropdown and goes to Upload First Draft
        WebElement dropdown2 = driver.findElement(By.id("navbarDropdown"));
        dropdown2.click();

        java.util.List<WebElement> dropdownItems2 = driver.findElements(By.className("dropdown-item"));
        WebElement currentphase = null;
        for (WebElement item : dropdownItems2) {
            if (item.getText().equals("Current Phase")) {
                currentphase = item;
                break;
            }
        }

        if (currentphase != null) currentphase.click();

        // checks if we are in upload first draft page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/phase", actualURL);
    }


    @Test
    public void test_login_planner_upload() {
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
        username.sendKeys(PlannerUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/", actualURL);

        // clicks dropdown and goes to Upload First Draft
        WebElement dropdown = driver.findElement(By.id("navbarDropdown"));
        dropdown.click();

        java.util.List<WebElement> dropdownItems = driver.findElements(By.className("dropdown-item"));
        WebElement uploaddraft = null;
        for (WebElement item : dropdownItems) {
            if (item.getText().equals("Upload First Draft")) {
                uploaddraft = item;
                break;
            }
        }

        if (uploaddraft != null) uploaddraft.click();

        // checks if we are in upload first draft page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/upload", actualURL);

        // upload NOTCSVFILE
        WebElement browse = driver.findElement(By.className("custom-file-input"));
        browse.sendKeys(NOTCSVFILE);

        // find and click upload button
        java.util.List<WebElement> buttons = driver.findElements(By.tagName("button"));

        WebElement uploadButton = null;
        for (WebElement item : buttons) {
            if (item.getText().equals("Upload")) {
                uploadButton = item;
                break;
            }
        }

        if (uploadButton != null) uploadButton.click();

        // check for alert saying 'This file is not a .csv file'
        java.util.List<WebElement> alerts = driver.findElements(By.className("alert-dismissible"));
        WebElement notCSValert = null;
        for (WebElement item : alerts){
            if (item.getText().startsWith("This file")){
                notCSValert = item;
                break;
            }
        }
        assertEquals("This file is not a .csv file", notCSValert.getText().substring(0,28));


        // upload WRONGCSVFILE
        WebElement browse2 = driver.findElement(By.className("custom-file-input"));
        browse2.sendKeys(WRONGCSVFILE);

        // find and click upload button
        java.util.List<WebElement> buttons2 = driver.findElements(By.tagName("button"));
        WebElement uploadButton2 = null;
        for (WebElement item : buttons2) {
            if (item.getText().equals("Upload")) {
                uploadButton2 = item;
                break;
            }
        }
        if (uploadButton2 != null) uploadButton2.click();

        // check for alert saying 'This file is not a .csv file'
        java.util.List<WebElement> alerts2 = driver.findElements(By.className("alert-dismissible"));
        WebElement notCSValert2 = null;
        for (WebElement item : alerts2){
            System.out.println(item.getText());
            if (item.getText().startsWith("Unable")){
                notCSValert2 = item;
                break;
            }
        }
        assertEquals("Unable to upload file", notCSValert2.getText().substring(0,21));

    }


    @Test
    public void test_login_prof() {
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

        // clicks dropdown and goes to view course details
        WebElement dropdown2 = driver.findElement(By.id("navbarDropdown"));
        dropdown2.click();
        java.util.List<WebElement> dropdownItems2 = driver.findElements(By.className("dropdown-item"));
        WebElement viewcourse = null;
        for (WebElement item : dropdownItems2) {
            if (item.getText().equals("View Submitted Details")) {
                viewcourse = item;
                break;
            }
        }

        if (viewcourse != null) viewcourse.click();

        // checks if we are in view course list page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/professors/details", actualURL);

        // clicks home
        WebElement home = driver.findElement(By.className("navbar-brand"));
        home.click();
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/professors/", actualURL);
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
    public void test_planner_phase(){
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
        username.sendKeys(PlannerUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/", actualURL);

        // clicks dropdown and goes to Current Phase
        WebElement dropdown = driver.findElement(By.id("navbarDropdown"));
        dropdown.click();

        java.util.List<WebElement> dropdownItems = driver.findElements(By.className("dropdown-item"));
        WebElement currentPhase = null;
        for (WebElement item : dropdownItems) {
            if (item.getText().equals("Current Phase")) {
                currentPhase = item;
                break;
            }
        }

        if (currentPhase != null) currentPhase.click();

        // checks if we are in the current phase page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/phase", actualURL);

        // checks that we are in Phase 1
        java.util.List<WebElement> pElements = driver.findElements(By.tagName("p"));
        WebElement phaseNumber = null;
        for (WebElement item : pElements){
            if (item.getText().startsWith("We are currently")){
                phaseNumber = item;
                break;
            }
        }
        assertTrue(phaseNumber.getText().contains("Phase 1"));

        // find Previous Phase button and click it
        java.util.List<WebElement> buttons = driver.findElements(By.tagName("button"));
        WebElement prevPhase = null;
        for (WebElement item : buttons){
            if (item.getText().startsWith("Previous Phase")){
                prevPhase = item;
                break;
            }
        }
        if (prevPhase != null) prevPhase.click();

        WebElement yesButton = driver.findElement(By.className("btn-danger"));
        yesButton.click();

        // checks that we are in still in Phase 1
        java.util.List<WebElement> pElements2 = driver.findElements(By.tagName("p"));
        WebElement phaseNumber2 = null;
        for (WebElement item : pElements2){
            if (item.getText().startsWith("We are currently")){
                phaseNumber2 = item;
                break;
            }
        }
        assertTrue(phaseNumber2.getText().contains("Phase 1"));

        // find Next Phase button and click it
        java.util.List<WebElement> buttons2 = driver.findElements(By.tagName("button"));
        WebElement nextPhase = null;
        for (WebElement item : buttons2){
            if (item.getText().startsWith("Next Phase")){
                nextPhase = item;
                break;
            }
        }
        if (nextPhase != null) nextPhase.click();

        WebElement yesButton2 = driver.findElement(By.id("NextModal")).findElement(By.className("btn-danger"));
        yesButton2.click();

        // checks that we are in Phase 2 now
        java.util.List<WebElement> pElements3 = driver.findElements(By.tagName("p"));
        WebElement phaseNumber3 = null;
        for (WebElement item : pElements3){
            if (item.getText().startsWith("We are currently")){
                phaseNumber3 = item;
                break;
            }
        }
        assertTrue(phaseNumber3.getText().contains("Phase 2"));


        // find Next Phase button and click it
        java.util.List<WebElement> buttons3 = driver.findElements(By.tagName("button"));
        WebElement nextPhase2 = null;
        for (WebElement item : buttons3){
            if (item.getText().startsWith("Next Phase")){
                nextPhase2 = item;
                break;
            }
        }
        if (nextPhase2 != null) nextPhase2.click();

        WebElement yesButton3 = driver.findElement(By.id("NextModal")).findElement(By.className("btn-danger"));
        yesButton3.click();

        // checks that we are in Phase 3 now
        java.util.List<WebElement> pElements4 = driver.findElements(By.tagName("p"));
        WebElement phaseNumber4 = null;
        for (WebElement item : pElements4){
            if (item.getText().startsWith("We are currently")){
                phaseNumber4 = item;
                break;
            }
        }
        assertTrue(phaseNumber4.getText().contains("Phase 3"));

        // ==== Try going to next phase when we are in Phase 3 already
        // find Next Phase button and click it
        buttons3 = driver.findElements(By.tagName("button"));
        nextPhase2 = null;
        for (WebElement item : buttons3){
            if (item.getText().startsWith("Next Phase")){
                nextPhase2 = item;
                break;
            }
        }
        if (nextPhase2 != null) nextPhase2.click();

        yesButton3 = driver.findElement(By.id("NextModal")).findElement(By.className("btn-danger"));
        yesButton3.click();

        // checks that we are still in Phase 3 now
        pElements4 = driver.findElements(By.tagName("p"));
        phaseNumber4 = null;
        for (WebElement item : pElements4){
            if (item.getText().startsWith("We are currently")){
                phaseNumber4 = item;
                break;
            }
        }
        assertTrue(phaseNumber4.getText().contains("Phase 3"));


        // ======= go back to Phase 1 =============
        // find Previous Phase button and click it
        java.util.List<WebElement> buttons4 = driver.findElements(By.tagName("button"));
        WebElement prevPhase2 = null;
        for (WebElement item : buttons4){
            if (item.getText().startsWith("Previous Phase")){
                prevPhase2 = item;
                break;
            }
        }
        if (prevPhase2 != null) prevPhase2.click();

        yesButton = driver.findElement(By.className("btn-danger"));
        yesButton.click();

        // checks that we are now in Phase 2
        pElements2 = driver.findElements(By.tagName("p"));
        phaseNumber2 = null;
        for (WebElement item : pElements2){
            if (item.getText().startsWith("We are currently")){
                phaseNumber2 = item;
                break;
            }
        }
        assertTrue(phaseNumber2.getText().contains("Phase 2"));

        // find Previous Phase button and click it
        buttons4 = driver.findElements(By.tagName("button"));
        prevPhase2 = null;
        for (WebElement item : buttons4){
            if (item.getText().startsWith("Previous Phase")){
                prevPhase2 = item;
                break;
            }
        }
        if (prevPhase2 != null) prevPhase2.click();

        yesButton = driver.findElement(By.className("btn-danger"));
        yesButton.click();

        // checks that we are now in Phase 1
        pElements2 = driver.findElements(By.tagName("p"));
        phaseNumber2 = null;
        for (WebElement item : pElements2){
            if (item.getText().startsWith("We are currently")){
                phaseNumber2 = item;
                break;
            }
        }
        assertTrue(phaseNumber2.getText().contains("Phase 1"));
    }

    @Test
    public void test_phase_revert(){
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
        username.sendKeys(PlannerUserName);

        WebElement password = driver.findElement(By.id("id_password"));
        password.clear();
        password.sendKeys(PASSWORD);

        WebElement LoginButton = driver.findElement(By.id("id_login"));
        LoginButton.click();

        // checks if we are in main page
        String actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/", actualURL);

        // clicks dropdown and goes to Current Phase
        WebElement dropdown = driver.findElement(By.id("navbarDropdown"));
        dropdown.click();

        java.util.List<WebElement> dropdownItems = driver.findElements(By.className("dropdown-item"));
        WebElement currentPhase = null;
        for (WebElement item : dropdownItems) {
            if (item.getText().equals("Current Phase")) {
                currentPhase = item;
                break;
            }
        }

        if (currentPhase != null) currentPhase.click();

        // checks if we are in the current phase page
        actualURL = driver.getCurrentUrl();
        assertNotNull(actualURL);
        assertEquals("http://127.0.0.1:8000/planners/phase", actualURL);

        // checks that we are in Phase 1
        java.util.List<WebElement> pElements = driver.findElements(By.tagName("p"));
        WebElement phaseNumber = null;
        for (WebElement item : pElements){
            if (item.getText().startsWith("We are currently")){
                phaseNumber = item;
                break;
            }
        }
        assertTrue(phaseNumber.getText().contains("Phase 1"));

        // find Next Phase button and click it
        java.util.List<WebElement> buttons2 = driver.findElements(By.tagName("button"));
        WebElement nextPhase = null;
        for (WebElement item : buttons2){
            if (item.getText().startsWith("Next Phase")){
                nextPhase = item;
                break;
            }
        }
        if (nextPhase != null) nextPhase.click();

        WebElement yesButton2 = driver.findElement(By.id("NextModal")).findElement(By.className("btn-danger"));
        yesButton2.click();

        // checks that we are in Phase 2 now
        java.util.List<WebElement> pElements3 = driver.findElements(By.tagName("p"));
        WebElement phaseNumber3 = null;
        for (WebElement item : pElements3){
            if (item.getText().startsWith("We are currently")){
                phaseNumber3 = item;
                break;
            }
        }
        assertTrue(phaseNumber3.getText().contains("Phase 2"));


        // find Next Phase button and click it
        java.util.List<WebElement> buttons3 = driver.findElements(By.tagName("button"));
        WebElement nextPhase2 = null;
        for (WebElement item : buttons3){
            if (item.getText().startsWith("Next Phase")){
                nextPhase2 = item;
                break;
            }
        }
        if (nextPhase2 != null) nextPhase2.click();

        WebElement yesButton3 = driver.findElement(By.id("NextModal")).findElement(By.className("btn-danger"));
        yesButton3.click();

        // checks that we are in Phase 3 now
        java.util.List<WebElement> pElements4 = driver.findElements(By.tagName("p"));
        WebElement phaseNumber4 = null;
        for (WebElement item : pElements4){
            if (item.getText().startsWith("We are currently")){
                phaseNumber4 = item;
                break;
            }
        }
        assertTrue(phaseNumber4.getText().contains("Phase 3"));

        // find the revert button and click it
        buttons3 = driver.findElements(By.tagName("button"));
        WebElement revert = null;
        for (WebElement item : buttons3){
            if (item.getText().startsWith("Revert")){
                revert = item;
                break;
            }
        }
        if (revert != null) revert.click();
        yesButton3 = driver.findElement(By.id("RevertModal")).findElement(By.className("btn-danger"));
        yesButton3.click();

        // checks that we are in Phase 1 now
        pElements4 = driver.findElements(By.tagName("p"));
        phaseNumber4 = null;
        for (WebElement item : pElements4){
            if (item.getText().startsWith("We are currently")){
                phaseNumber4 = item;
                break;
            }
        }
        assertTrue(phaseNumber4.getText().contains("Phase 1"));


    }

}
