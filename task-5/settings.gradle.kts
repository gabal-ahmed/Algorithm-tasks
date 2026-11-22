pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "NavigationDrawerDemo"

// The Android module needs an Android SDK (sdk.dir in local.properties or ANDROID_HOME).
val hasSdk = System.getenv("ANDROID_HOME") != null || file("local.properties").exists()
if (hasSdk) include(":app")
include(":desktop-preview")
