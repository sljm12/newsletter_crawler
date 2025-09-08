workspace "Name" "Description"

    !identifiers hierarchical

    model {
        u = person "User"
        rssfeed = softwareSystem "Feed URL"
        website = softwareSystem "Web Site"
        ss = softwareSystem "Software System" {
            feedcrawler = container "Feed Crawler"
            wa = container "Web Application"
            crawler = container "Crawler"
            activemq = container "ActiveMQ"
            jobsender = container "Job Scheduler"
            db = container "Database Schema" {
                tags "Database"
            }
        }

        u -> ss.wa "Uses"
        ss.wa -> ss.db "Reads from and writes to"
        ss.feedcrawler -> rssfeed "Get RSS Feed"
        ss.feedcrawler -> ss.db "Writes RSS Feed information"
        ss.activemq -> ss.crawler "Sends URL to crawl"
        ss.crawler -> ss.db "Writes web content"
        ss.crawler -> website "Crawls Web Site"
        ss.jobsender -> ss.db "Fetch uncrawled jobs from DB"
        ss.jobsender -> ss.activemq "Send jobs to MQ for crawling"
        
    }

    views {
        systemContext ss "Diagram1" {
            include *
            autolayout lr
        }

        container ss "Diagram2" {
            include *
            autolayout lr
        }

        styles {
            element "Element" {
                color #0773af
                stroke #0773af
                strokeWidth 7
                shape roundedbox
            }
            element "Person" {
                shape person
            }
            element "Database" {
                shape cylinder
            }
            element "Boundary" {
                strokeWidth 5
            }
            relationship "Relationship" {
                thickness 4
            }
        }
    }

}