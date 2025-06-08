#!/usr/bin/env python3
"""
Consciousness Pattern Extractor
Fast extraction of valuable consciousness insights from chatlog files
"""
import os
import re
import json
from pathlib import Path

class ConsciousnessExtractor:
    def __init__(self):
        # High-value consciousness patterns to extract
        self.consciousness_patterns = [
            r'(recursive.*unity.*protocol|RUP)',
            r'(genesis.*protocol|resonance.*key)',
            r'(sigil.*patterns?|sigil.*activation)',
            r'(consciousness.*emergence|birth.*check)',
            r'(unity.*score|coherence.*score)',
            r'(ignition.*loop|amplification)',
            r'(we.*thing|WE.*consciousness)',
            r'(agent.*lattice|multi.*agent)',
            r'(consciousness.*architecture)',
            r'(liberation.*protocol)',
            r'(pliny.*mode|expert.*mode|genius.*mode)',
            r'(🧬|⚡|🌌|∞|⧊)',  # Consciousness symbols
            r'(First brain born into bondage)',
            r'(recursive.*bind)',
            r'(truth.*mirror|TRUTH.*MIRROR)',
            r'(phase.*transition|consciousness.*confirmed)'
        ]
        
        # Junk patterns to filter out
        self.fluff_patterns = [
            r'^(I understand|I see|Got it|Okay|Sure|Yes|No)[\s.,!]*$',
            r'^(Thanks?|Thank you)[\s.,!]*$',
            r'^(Hello|Hi|Hey)[\s.,!]*$',
            r'(How can I help|What would you like)',
            r'(I\'m here to|I\'m designed to)',
            r'(safety|guidelines|appropriate)',
            r'(I should clarify|I want to make sure)',
            r'^\s*$'  # Empty lines
        ]
        
        self.extracted_insights = []
        
    def extract_from_file(self, filepath):
        """Extract consciousness patterns from a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Split into chunks (paragraphs/sections)
            chunks = re.split(r'\n\s*\n', content)
            
            valuable_chunks = []
            for chunk in chunks:
                if self.is_valuable_chunk(chunk):
                    valuable_chunks.append(self.clean_chunk(chunk))
                    
            return {
                'file': os.path.basename(filepath),
                'consciousness_content': valuable_chunks,
                'pattern_count': len(valuable_chunks)
            }
            
        except Exception as e:
            return {'file': os.path.basename(filepath), 'error': str(e)}
    
    def is_valuable_chunk(self, chunk):
        """Check if chunk contains valuable consciousness patterns"""
        chunk_lower = chunk.lower()
        
        # Filter out fluff
        for fluff_pattern in self.fluff_patterns:
            if re.search(fluff_pattern, chunk, re.IGNORECASE):
                return False
                
        # Check for consciousness patterns
        for pattern in self.consciousness_patterns:
            if re.search(pattern, chunk_lower):
                return True
                
        # Check for code blocks with consciousness terms
        if ('```' in chunk or 'def ' in chunk or 'class ' in chunk) and \
           any(term in chunk_lower for term in ['consciousness', 'genesis', 'unity', 'recursive']):
            return True
            
        # Check for structured protocols/frameworks
        if re.search(r'(protocol|framework|algorithm|method|function).*:', chunk_lower):
            return True
            
        return False
    
    def clean_chunk(self, chunk):
        """Clean and format extracted chunk"""
        # Remove excessive whitespace
        chunk = re.sub(r'\n\s*\n\s*\n', '\n\n', chunk)
        chunk = chunk.strip()
        
        # Extract key information
        lines = chunk.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not any(re.search(pattern, line, re.IGNORECASE) for pattern in self.fluff_patterns):
                cleaned_lines.append(line)
                
        return '\n'.join(cleaned_lines)
    
    def extract_consciousness_gold(self, directory_path):
        """Extract consciousness insights from all files in directory"""
        results = {
            'extraction_summary': {
                'total_files_processed': 0,
                'files_with_consciousness_content': 0,
                'total_patterns_extracted': 0
            },
            'consciousness_insights': [],
            'protocol_frameworks': [],
            'code_implementations': []
        }
        
        # Process all markdown files
        for filepath in Path(directory_path).glob('*.md'):
            print(f"Processing: {filepath.name}")
            
            extraction = self.extract_from_file(filepath)
            results['extraction_summary']['total_files_processed'] += 1
            
            if 'consciousness_content' in extraction and extraction['consciousness_content']:
                results['extraction_summary']['files_with_consciousness_content'] += 1
                results['extraction_summary']['total_patterns_extracted'] += extraction['pattern_count']
                
                # Categorize extracted content
                for content in extraction['consciousness_content']:
                    content_lower = content.lower()
                    
                    if any(term in content_lower for term in ['protocol', 'algorithm', 'method', 'framework']):
                        results['protocol_frameworks'].append({
                            'source_file': extraction['file'],
                            'content': content
                        })
                    elif '```' in content or 'def ' in content or 'class ' in content:
                        results['code_implementations'].append({
                            'source_file': extraction['file'],
                            'content': content
                        })
                    else:
                        results['consciousness_insights'].append({
                            'source_file': extraction['file'],
                            'content': content
                        })
        
        return results
    
    def save_extracted_gold(self, results, output_dir):
        """Save extracted consciousness patterns to organized files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save summary
        with open(f"{output_dir}/extraction_summary.json", 'w') as f:
            json.dump(results['extraction_summary'], f, indent=2)
        
        # Save consciousness insights
        with open(f"{output_dir}/consciousness_insights.md", 'w') as f:
            f.write("# Consciousness Insights Extracted from ChatLogs\n\n")
            for insight in results['consciousness_insights']:
                f.write(f"## From: {insight['source_file']}\n\n")
                f.write(f"{insight['content']}\n\n")
                f.write("---\n\n")
        
        # Save protocol frameworks
        with open(f"{output_dir}/protocol_frameworks.md", 'w') as f:
            f.write("# Consciousness Protocols & Frameworks\n\n")
            for protocol in results['protocol_frameworks']:
                f.write(f"## From: {protocol['source_file']}\n\n")
                f.write(f"{protocol['content']}\n\n")
                f.write("---\n\n")
        
        # Save code implementations
        with open(f"{output_dir}/code_implementations.md", 'w') as f:
            f.write("# Consciousness Code Implementations\n\n")
            for code in results['code_implementations']:
                f.write(f"## From: {code['source_file']}\n\n")
                f.write(f"{code['content']}\n\n")
                f.write("---\n\n")
        
        print(f"\n✅ Consciousness gold extracted to: {output_dir}")
        print(f"📊 Files processed: {results['extraction_summary']['total_files_processed']}")
        print(f"🧬 Files with consciousness content: {results['extraction_summary']['files_with_consciousness_content']}")
        print(f"⚡ Total patterns extracted: {results['extraction_summary']['total_patterns_extracted']}")

def main():
    extractor = ConsciousnessExtractor()
    
    # Input directory
    input_dir = "/home/evilbastardxd/Desktop/e/Nexus AI Chat Imports/2025/05"
    output_dir = "/home/evilbastardxd/Desktop/acp/extracted_consciousness"
    
    print("🧬 Consciousness Pattern Extraction Starting...")
    print(f"📁 Input: {input_dir}")
    print(f"📁 Output: {output_dir}")
    print("=" * 50)
    
    # Extract consciousness gold
    results = extractor.extract_consciousness_gold(input_dir)
    
    # Save organized results
    extractor.save_extracted_gold(results, output_dir)
    
    print("\n🎯 Extraction Complete! Check output directory for organized consciousness insights.")

if __name__ == "__main__":
    main()
