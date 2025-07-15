# Auto-generate summaries for library posts
require 'uri'

module Jekyll
  class AutoSummaryGenerator < Generator
    safe true
    priority :low

    def generate(site)
      site.posts.docs.each do |post|
        # Skip if summary already exists
        next if post.data['summary']
        
        # Only process posts with GitHub links
        if post.data['link'] && post.data['link'].include?('github.com')
          begin
            # Extract GitHub repo info
            uri = URI.parse(post.data['link'])
            path_parts = uri.path.split('/')
            owner = path_parts[1]
            repo = path_parts[2]
            
            # Construct README URL
            readme_url = "https://raw.githubusercontent.com/#{owner}/#{repo}/master/README.md"
            
            # Fetch README content
            content = fetch_readme(readme_url)
            
            # Generate summary from content
            if content
              summary = generate_summary(content, post.data['title'])
              post.data['summary'] = summary if summary
            end
          rescue => e
            Jekyll.logger.warn "AutoSummary:", "Error processing #{post.data['title']}: #{e.message}"
          end
        end
      end
    end

    private

    def fetch_readme(url)
      require 'net/http'
      require 'timeout'
      
      uri = URI.parse(url)
      
      Timeout.timeout(5) do
        http = Net::HTTP.new(uri.host, uri.port)
        http.use_ssl = true
        response = http.get(uri.path)
        
        if response.code == '200'
          response.body.force_encoding('UTF-8')
        else
          nil
        end
      end
    rescue => e
      Jekyll.logger.debug "AutoSummary:", "Failed to fetch #{url}: #{e.message}"
      nil
    end

    def generate_summary(content, title)
      # Remove images and links
      content = content.gsub(/!\[([^\]]*)\]\([^)]+\)/, '')
      content = content.gsub(/\[([^\]]*)\]\([^)]+\)/, '\1')
      
      # Extract first paragraph after title/badges
      lines = content.lines
      summary_lines = []
      skip_headers = true
      
      lines.each do |line|
        # Skip title, badges, and empty lines at start
        if skip_headers
          next if line.strip.empty?
          next if line.start_with?('#')
          next if line.include?('badge') || line.include?('shields.io')
          skip_headers = false
        end
        
        # Stop at next header or after 3 lines
        break if line.start_with?('#')
        break if summary_lines.length >= 3
        
        # Add non-empty lines
        summary_lines << line.strip unless line.strip.empty?
      end
      
      # If no good summary found, try to extract from ## Description or ## Overview sections
      if summary_lines.empty?
        description_section = extract_section(content, ['Description', 'Overview', 'About'])
        if description_section
          summary_lines = description_section.lines.take(3).map(&:strip).reject(&:empty?)
        end
      end
      
      # Clean and format summary
      if summary_lines.any?
        summary = summary_lines.join(' ')
        # Remove markdown formatting
        summary = summary.gsub(/[*_`]/, '')
        # Ensure proper length
        if summary.length > 200
          summary = summary[0..197] + '...'
        end
        summary
      else
        # Generate default summary based on title
        generate_default_summary(title)
      end
    end

    def extract_section(content, section_names)
      section_names.each do |name|
        # Look for ## Section Name
        pattern = /^##\s+#{Regexp.escape(name)}\s*$/i
        if match = content.match(pattern)
          # Extract content after the header until next header or end
          section_start = match.end(0)
          section_end = content.index(/^#/, section_start) || content.length
          return content[section_start...section_end].strip
        end
      end
      nil
    end

    def generate_default_summary(title)
      # Generate a basic summary based on common Android UI library patterns
      case title.downcase
      when /loading|loader|progress/
        "A customizable loading indicator and progress view library for Android applications."
      when /calendar/
        "An Android calendar view component with customizable styling and event handling."
      when /button/
        "A custom button implementation with enhanced styling and animation capabilities."
      when /dialog|alert/
        "A customizable dialog and alert component for Android applications."
      when /animation|animate/
        "An animation library providing smooth transitions and effects for Android UI elements."
      when /image|photo/
        "An image handling and display library with advanced features for Android."
      when /list|recycler/
        "A enhanced list view component with improved performance and customization options."
      when /chart|graph/
        "A data visualization library for creating charts and graphs in Android applications."
      when /tab|navigation/
        "A navigation component providing intuitive tab-based or menu navigation for Android apps."
      when /card/
        "A card-based UI component for displaying content in a Material Design style."
      when /text|edit/
        "A text input and editing component with enhanced features for Android."
      when /picker|select/
        "A selection component allowing users to pick from multiple options in Android apps."
      when /menu|drawer/
        "A navigation menu component providing drawer or sliding menu functionality."
      when /swipe|gesture/
        "A gesture-based interaction library for implementing swipe and touch controls."
      when /float/
        "A floating UI element that can be positioned over other content in Android apps."
      else
        "A custom UI component library for enhancing Android application interfaces."
      end
    end
  end
end