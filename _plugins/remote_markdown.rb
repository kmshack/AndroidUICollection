# "THE BEER-WARE LICENSE" (Revision 42):
# <robin.hahling@gw-computing.net> wrote this file. As long as you retain this
# notice you can do whatever you want with this stuff. If we meet some day, and
# you think this stuff is worth it, you can buy me a beer in return.
# Robin Hahling

require 'net/http'

module Jekyll
  # Remotely fetch a markdown file.
  class RemoteMarkdownTag < Liquid::Tag
    def initialize(tag_name, text, tokens)
      super
    
      puts "download >> #{text}"
      
      text.strip!
      check_protocol(text)
      uri = URI(text)

      check_extension(uri.path)

      res = Net::HTTP.get_response(uri)
      fail 'resource unavailable' unless res.is_a?(Net::HTTPSuccess)

        md = res.body.force_encoding("UTF-8")
        md = md.gsub! '!', ''
        @content = md
            
    end

    def render(_context)
      @content
        
    end

    private

    def check_protocol(text)
      error_message = "remote_markdown: invalid URI given #{text}"
      fail error_message unless text =~ URI.regexp(%w(http https ftp ftps))
    end

    def check_extension(path)
      mdexts = %w(.markdown .mkdown .mkdn .mkd .md .MD)
      error_message = "remote_markdown: URI file extension not in #{mdexts}"
      fail error_message unless mdexts.include?(File.extname(path))
    end
  end
end

Liquid::Template.register_tag('remote_markdown', Jekyll::RemoteMarkdownTag)
