library(mongolite)
library(ggplot2)
library(signal)

# Connect to MongoDB
mongo <- mongo(collection = "Measured values", db = "IoT", url = 'mongodb+srv://Admin:Domusa96lewe-@cluster0.xf9oyhe.mongodb.net/test')

# Fetch all documents from the collection and put it into a dataframe
data <- mongo$find()

# Close the connection
mongo$disconnect()

# Convert timestamps to POSIXct with proper time zone conversion
data$timestamp <- as.POSIXct(data$timestamp / 1000, origin = "1970-01-01", tz = "UTC")

# Convert to Switzerland time zone (CET/CEST)
data$timestamp <- as.POSIXct(format(data$timestamp, tz = "Europe/Zurich"), tz = "Europe/Zurich")

# Calculate rate of change in pressure
data$pressure_diff <- c(NA, diff(data$pressure)) # Calculate difference between consecutive pressure values

# Define threshold for significant pressure change
threshold <- 0.2 # You can adjust this threshold based on your data

# Identify positions where pressure change exceeds the threshold
data$significant_change <- ifelse(abs(data$pressure_diff) > threshold, 1, 0)

# Visualize pressure and significant changes over time
ggplot(data, aes(x = timestamp)) +
  geom_line(aes(y = pressure), color = "blue") +
  geom_point(aes(y = ifelse(significant_change == 1, pressure, NA)), color = "red") +
  labs(title = "Pressure over time with significant changes", x = "Timestamp", y = "Pressure") +
  theme_minimal()
