require 'asciidoctor'
require 'asciidoctor/extensions'

Asciidoctor::Extensions.register do
  inline_macro do
    named :syl

    process do |parent, target, attrs|
      colors = %w[
        #e53935
        #1e88e5
        #43a047
        #fb8c00
        #8e24aa
      ]

      color_index = 0
      output = []

      # Separar palabras por _ y sílabas por .
      words = target.split('_')

      words.each_with_index do |word, wi|
        syllables = word.split('.')
        syllables.each do |syll|
          color = colors[color_index % colors.length]
          output << %(<span style="color: #{color}">#{syll}</span>)
          color_index += 1
        end
        # espacio entre palabras
        output << ' ' if wi < words.size - 1
      end

      create_inline parent, :quoted, output.join, type: :unquoted
    end
  end
end
