#!/usr/bin/env python3
"""
Script to extract unique team abbreviations from baseball CSV files across all years.
Only keeps teams that follow the AAA_BBB format, are D1 level, and skips unverified files.
Extracts Stadium, Level, and League information.
"""

import csv
import os
import re
from pathlib import Path
from typing import Set, Dict, Tuple

def is_valid_team_format(team: str) -> bool:
    """
    Check if team abbreviation follows the AAA_BBB format.
    
    Args:
        team: Team abbreviation to check
        
    Returns:
        True if team follows AAA_BBB format, False otherwise
    """
    # Pattern: exactly 3 letters, underscore, exactly 3 letters
    pattern = r'^[A-Za-z]{3}_[A-Za-z]{3}$'
    return bool(re.match(pattern, team))

def extract_team_data(csv_folder_path: str) -> Dict[str, Dict[str, str]]:
    """
    Extract unique team abbreviations and their info from all CSV files in all year folders.
    Only includes D1 teams that follow AAA_BBB format and skips unverified files.
    
    Args:
        csv_folder_path: Path to the folder containing year subdirectories with CSV files
        
    Returns:
        Dictionary mapping team abbreviations to their info (Stadium, Level, League)
    """
    team_info_map = {}
    csv_folder = Path(csv_folder_path)
    
    # Get all year directories
    year_dirs = [d for d in csv_folder.iterdir() if d.is_dir()]
    
    if not year_dirs:
        print(f"No year directories found in {csv_folder_path}")
        return team_info_map
    
    print(f"Processing {len(year_dirs)} year directories...")
    
    total_files_processed = 0
    skipped_files = 0
    d1_teams_found = 0
    
    for year_dir in sorted(year_dirs):
        print(f"\nProcessing year: {year_dir.name}")
        
        # Get all CSV files in this year directory
        csv_files = list(year_dir.glob("*.csv"))
        
        if not csv_files:
            print(f"  No CSV files found in {year_dir.name}")
            continue
            
        print(f"  Found {len(csv_files)} CSV files in {year_dir.name}")
        
        for csv_file in csv_files:
            # Skip files with "unverified" in the name (case insensitive)
            if "unverified" in csv_file.name.lower():
                skipped_files += 1
                continue
                
            try:
                with open(csv_file, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    first_row = next(reader, None)
                    
                    if first_row:
                        # Check if this is a D1 game
                        level = first_row.get('Level', '').strip()
                        if level != 'D1':
                            continue
                        
                        # Extract common info
                        stadium = first_row.get('Stadium', '').strip()
                        league = first_row.get('League', '').strip()
                        
                        # Process HomeTeam
                        if 'HomeTeam' in first_row:
                            home_team = first_row['HomeTeam'].strip()
                            if home_team and is_valid_team_format(home_team):
                                if home_team not in team_info_map:
                                    team_info_map[home_team] = {
                                        'Stadium': stadium,
                                        'Level': level,
                                        'League': league
                                    }
                                    d1_teams_found += 1
                        
                        total_files_processed += 1
                        
                        if total_files_processed % 100 == 0:
                            print(f"  Processed {total_files_processed} D1 files so far...")
                
            except Exception as e:
                print(f"  Error processing {csv_file.name}: {e}")
    
    print(f"\nTotal D1 files processed: {total_files_processed}")
    print(f"Total files skipped (unverified): {skipped_files}")
    print(f"Total unique D1 team abbreviations found (AAA_BBB format): {len(team_info_map)}")
    
    return team_info_map

def write_to_csv(data: Dict[str, Dict[str, str]], output_path: str):
    """
    Write the team abbreviations and their info to a CSV file.
    
    Args:
        data: Dictionary mapping team abbreviations to their info
        output_path: Path where to save the CSV file
    """
    # Sort data for consistent output
    sorted_data = sorted(data.items())
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['TrackmanAbbreviation', 'Stadium', 'Level', 'League'])
        
        # Write data
        for team, info in sorted_data:
            writer.writerow([
                team,
                info['Stadium'],
                info['Level'],
                info['League']
            ])
    
    print(f"\nCSV file saved to: {output_path}")
    print(f"Total records written: {len(sorted_data)}")

def main():
    # Path to CSV folder relative to the scripts folder
    csv_folder_path = "../csv"
    
    # Output CSV path (root directory)
    output_csv_path = "../d1_team_abbreviations.csv"
    
    # Extract the data
    team_data = extract_team_data(csv_folder_path)
    
    # Write to CSV file
    write_to_csv(team_data, output_csv_path)
    
    # Display summary to console
    sorted_teams = sorted(team_data.items())
    
    print(f"\n{'='*80}")
    print(f"SUMMARY: Found {len(sorted_teams)} unique D1 team abbreviations (AAA_BBB format):")
    print(f"{'='*80}")
    
    for i, (team, info) in enumerate(sorted_teams, 1):
        print(f"{i:3d}. {team:15} | Stadium: {info['Stadium']:30} | League: {info['League']}")

if __name__ == "__main__":
    main()