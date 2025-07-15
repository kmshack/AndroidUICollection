# Enhanced remote markdown fetcher with caching and better error handling
# Based on original by Robin Hahling

require 'net/http'
require 'uri'
require 'fileutils'
require 'digest/md5'
require 'timeout'

module Jekyll
  class RemoteMarkdownTag < Liquid::Tag
    # Configuration
    CACHE_DIR = '_remote_markdown_cache'
    CACHE_EXPIRY = 3600 * 24 * 7  # 7 days in seconds
    TIMEOUT_SECONDS = 10
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    # Markdown extensions
    MARKDOWN_EXTENSIONS = %w[.markdown .mkdown .mkdn .mkd .md .MD].freeze
    
    # User agent for requests
    USER_AGENT = 'AndroidUICollection-Jekyll/1.0'
    
    def initialize(tag_name, text, tokens)
      super
      @url = text.strip
      validate_url
      
      # Initialize cache directory
      FileUtils.mkdir_p(CACHE_DIR) unless Dir.exist?(CACHE_DIR)
      
      # Fetch content
      @content = fetch_with_cache(@url)
    end

    def render(_context)
      @content
    end

    private

    def validate_url
      raise ArgumentError, "No URL provided" if @url.empty?
      
      uri = URI.parse(@url)
      unless %w[http https].include?(uri.scheme)
        raise ArgumentError, "Invalid protocol: #{uri.scheme}. Only HTTP(S) allowed."
      end
      
      unless MARKDOWN_EXTENSIONS.include?(File.extname(uri.path).downcase)
        raise ArgumentError, "Invalid file extension. Expected markdown file."
      end
    rescue URI::InvalidURIError => e
      raise ArgumentError, "Invalid URL: #{@url} - #{e.message}"
    end

    def fetch_with_cache(url)
      cache_key = Digest::MD5.hexdigest(url)
      cache_file = File.join(CACHE_DIR, "#{cache_key}.md")
      cache_meta_file = File.join(CACHE_DIR, "#{cache_key}.meta")
      
      # Check if cache exists and is valid
      if cache_valid?(cache_file, cache_meta_file)
        Jekyll.logger.info "RemoteMarkdown:", "Using cached content for #{url}"
        return File.read(cache_file, encoding: 'UTF-8')
      end
      
      # Fetch fresh content
      Jekyll.logger.info "RemoteMarkdown:", "Fetching #{url}"
      content = fetch_remote_content(url)
      
      # Save to cache
      if content && !content.start_with?('<!--')
        save_to_cache(cache_file, cache_meta_file, content)
      end
      
      content
    end

    def cache_valid?(cache_file, cache_meta_file)
      return false unless File.exist?(cache_file) && File.exist?(cache_meta_file)
      
      # Check cache expiry
      metadata = JSON.parse(File.read(cache_meta_file))
      cached_time = Time.at(metadata['timestamp'])
      
      Time.now - cached_time < CACHE_EXPIRY
    rescue JSON::ParserError
      false
    end

    def save_to_cache(cache_file, cache_meta_file, content)
      File.write(cache_file, content)
      File.write(cache_meta_file, JSON.generate({
        'timestamp' => Time.now.to_i,
        'url' => @url
      }))
    rescue => e
      Jekyll.logger.warn "RemoteMarkdown:", "Failed to save cache: #{e.message}"
    end

    def fetch_remote_content(url)
      retries = 0
      
      begin
        uri = URI.parse(url)
        
        Timeout.timeout(TIMEOUT_SECONDS) do
          http = Net::HTTP.new(uri.host, uri.port)
          http.use_ssl = (uri.scheme == 'https')
          http.open_timeout = TIMEOUT_SECONDS
          http.read_timeout = TIMEOUT_SECONDS
          
          request = Net::HTTP::Get.new(uri.request_uri)
          request['User-Agent'] = USER_AGENT
          request['Accept'] = 'text/plain, text/markdown'
          
          response = http.request(request)
          
          case response
          when Net::HTTPSuccess
            content = response.body.force_encoding('UTF-8')
            process_markdown_content(content)
          when Net::HTTPRedirection
            # Follow redirect (max 1 level)
            if response['location'] && retries == 0
              Jekyll.logger.info "RemoteMarkdown:", "Following redirect to #{response['location']}"
              return fetch_remote_content(response['location'])
            else
              error_content("Too many redirects")
            end
          else
            error_content("HTTP #{response.code}: #{response.message}")
          end
        end
      rescue Timeout::Error
        error_content("Request timeout after #{TIMEOUT_SECONDS} seconds")
      rescue => e
        retries += 1
        if retries < MAX_RETRIES
          Jekyll.logger.warn "RemoteMarkdown:", "Retry #{retries}/#{MAX_RETRIES} for #{url}"
          sleep(RETRY_DELAY * retries)
          retry
        else
          error_content("Failed after #{MAX_RETRIES} attempts: #{e.message}")
        end
      end
    end

    def process_markdown_content(content)
      # Remove images by default (as in original)
      # This prevents broken image links from external repos
      content = content.gsub(/!\[([^\]]*)\]\([^)]+\)/, '[\1]')
      
      # Remove any potentially problematic HTML
      content = content.gsub(/<script[^>]*>.*?<\/script>/mi, '')
      content = content.gsub(/<iframe[^>]*>.*?<\/iframe>/mi, '')
      
      # Ensure content ends with newline
      content.chomp + "\n"
    end

    def error_content(message)
      Jekyll.logger.error "RemoteMarkdown:", "#{message} for #{@url}"
      
      # Return user-friendly error message
      <<~ERROR
        <!-- RemoteMarkdown Error: #{message} -->
        <div class="remote-markdown-error">
          <p><strong>Unable to load content from:</strong></p>
          <p><code>#{@url}</code></p>
          <p><em>#{message}</em></p>
        </div>
      ERROR
    end
  end
  
  # Cache cleanup task
  class RemoteMarkdownCacheCleanup < Generator
    safe true
    priority :low
    
    def generate(site)
      return unless Dir.exist?(RemoteMarkdownTag::CACHE_DIR)
      
      Dir.glob(File.join(RemoteMarkdownTag::CACHE_DIR, '*.meta')).each do |meta_file|
        begin
          metadata = JSON.parse(File.read(meta_file))
          cached_time = Time.at(metadata['timestamp'])
          
          # Remove expired cache files
          if Time.now - cached_time > RemoteMarkdownTag::CACHE_EXPIRY
            cache_file = meta_file.sub('.meta', '.md')
            File.delete(meta_file) if File.exist?(meta_file)
            File.delete(cache_file) if File.exist?(cache_file)
            Jekyll.logger.info "RemoteMarkdown:", "Cleaned expired cache for #{metadata['url']}"
          end
        rescue => e
          Jekyll.logger.warn "RemoteMarkdown:", "Error cleaning cache: #{e.message}"
        end
      end
    end
  end
end

Liquid::Template.register_tag('remote_markdown', Jekyll::RemoteMarkdownTag)