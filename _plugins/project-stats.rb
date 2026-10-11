# Computes publication statistics for each project page from the papers it cites
# with {% cite key %}: active years, number of papers and number of unique co-authors.
# A project can override the year range with a `years` field in its front matter.
require 'bibtex'

module Jekyll
  class ProjectStatsGenerator < Generator
    safe true
    priority :low

    # Authors matching these normalized names are the site owner (including her maiden name).
    SELF_NAMES = ['antsiferova a', 'zvezdakova a'].freeze

    TRANSLIT = {
      'а' => 'a', 'б' => 'b', 'в' => 'v', 'г' => 'g', 'д' => 'd', 'е' => 'e', 'ё' => 'e',
      'ж' => 'zh', 'з' => 'z', 'и' => 'i', 'й' => 'y', 'к' => 'k', 'л' => 'l', 'м' => 'm',
      'н' => 'n', 'о' => 'o', 'п' => 'p', 'р' => 'r', 'с' => 's', 'т' => 't', 'у' => 'u',
      'ф' => 'f', 'х' => 'kh', 'ц' => 'ts', 'ч' => 'ch', 'ш' => 'sh', 'щ' => 'shch', 'ъ' => '',
      'ы' => 'y', 'ь' => '', 'э' => 'e', 'ю' => 'yu', 'я' => 'ya'
    }.freeze

    def generate(site)
      projects = site.collections['projects']
      return unless projects

      scholar = site.config['scholar'] || {}
      bib_path = File.join(site.source, scholar['source'] || '_bibliography', scholar['bibliography'] || 'papers.bib')
      return unless File.exist?(bib_path)

      entries = {}
      BibTeX.open(bib_path).each do |entry|
        next unless entry.respond_to?(:key)
        entries[entry.key.to_s] = entry
      end

      projects.docs.each do |doc|
        keys = doc.content.scan(/\{%\s*cite\s+(.+?)\s*%\}/m).flatten.flat_map(&:split).uniq
        papers = keys.map { |k| entries[k] }.compact

        years = papers.map { |e| e[:year].to_s.to_i }.reject(&:zero?)
        if doc.data['years']
          doc.data['stats_years'] = doc.data['years'].to_s
        elsif years.any?
          doc.data['stats_years'] = years.min == years.max ? years.min.to_s : "#{years.min}–#{years.max}"
        end

        coauthors = papers.flat_map do |e|
          next [] unless e[:author]
          e.author.map { |name| normalize(name) }
        end
        coauthors = coauthors.uniq - SELF_NAMES

        doc.data['stats_papers'] = papers.size
        doc.data['stats_coauthors'] = coauthors.size
      end
    end

    private

    def normalize(name)
      last = translit(name.last.to_s)
      first = translit(name.first.to_s)
      "#{last} #{first[0]}"
    end

    def translit(str)
      str.downcase.chars.map { |c| TRANSLIT.fetch(c, c) }.join.gsub(/[^a-z]/, '')
    end
  end
end
