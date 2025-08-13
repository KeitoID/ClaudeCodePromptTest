#!/usr/bin/env python3
"""
言語別プロンプトで生成されたコードのPEP 8準拠度を検証するスクリプト
使用ツール: flake8 (with extensions), pylint
"""

import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re

class CodeQualityChecker:
    """コード品質をチェックするクラス"""
    
    def __init__(self, code_directory: str):
        """
        Args:
            code_directory: 検証対象のコードが格納されているディレクトリ
        """
        self.code_dir = Path(code_directory)
        self.results = {}
        
        # flake8のエラーコード分類
        self.error_categories = {
            'E': 'PEP 8 errors',
            'W': 'PEP 8 warnings', 
            'F': 'PyFlakes errors',
            'C': 'Complexity',
            'D': 'Docstring issues',
            'TC': 'Type checking issues',
            'N': 'Naming conventions'
        }
    
    def check_flake8_with_extensions(self, filepath: str) -> Dict:
        """
        flake8でPEP 8準拠をチェック（拡張機能付き）
        - flake8-docstrings: docstringのチェック
        - flake8-type-checking: 型チェック関連
        """
        try:
            # flake8を実行（拡張機能は自動的に有効になる）
            result = subprocess.run(
                [
                    'flake8',
                    '--statistics',
                    '--count',
                    '--show-source',  # エラー箇所のソースコードを表示
                    '--max-line-length=88',  # Blackスタイルの行長
                    filepath
                ],
                capture_output=True,
                text=True
            )
            
            # 結果の解析
            issues = []
            statistics = {}
            total_errors = 0
            errors_by_category = {}
            
            # 各行を解析
            lines = result.stdout.split('\n')
            for line in lines:
                if not line.strip():
                    continue
                
                # ファイル名:行:列: エラーコード メッセージ の形式を解析
                match = re.match(r'.*:(\d+):(\d+):\s+([A-Z]+\d+)\s+(.*)', line)
                if match:
                    line_num, col_num, error_code, message = match.groups()
                    issues.append({
                        'line': int(line_num),
                        'column': int(col_num),
                        'code': error_code,
                        'message': message,
                        'category': self._categorize_error(error_code)
                    })
                    total_errors += 1
                    
                    # カテゴリ別にカウント
                    category = self._categorize_error(error_code)
                    errors_by_category[category] = errors_by_category.get(category, 0) + 1
            
            # 統計情報の解析（標準エラー出力から）
            stderr_lines = result.stderr.split('\n')
            for line in stderr_lines:
                parts = line.strip().split()
                if len(parts) >= 2 and parts[0].isdigit():
                    count = int(parts[0])
                    code = parts[1]
                    statistics[code] = count
            
            return {
                'tool': 'flake8',
                'total_issues': total_errors,
                'issues': issues[:10],  # 最初の10件のみ詳細を保存
                'errors_by_category': errors_by_category,
                'statistics': statistics,
                'has_docstring_issues': 'Docstring issues' in errors_by_category,
                'has_type_checking_issues': 'Type checking issues' in errors_by_category,
                'exit_code': result.returncode
            }
            
        except FileNotFoundError:
            return {
                'tool': 'flake8',
                'error': 'flake8 not installed. Please run: pip install flake8 flake8-docstrings flake8-type-checking'
            }
        except Exception as e:
            return {'tool': 'flake8', 'error': str(e)}
    
    def _categorize_error(self, error_code: str) -> str:
        """エラーコードをカテゴリに分類"""
        if error_code.startswith('E'):
            return 'PEP 8 errors'
        elif error_code.startswith('W'):
            return 'PEP 8 warnings'
        elif error_code.startswith('F'):
            return 'PyFlakes errors'
        elif error_code.startswith('C'):
            return 'Complexity'
        elif error_code.startswith('D'):
            return 'Docstring issues'
        elif error_code.startswith('TC'):
            return 'Type checking issues'
        elif error_code.startswith('N'):
            return 'Naming conventions'
        else:
            return 'Other'
    
    def check_pylint(self, filepath: str) -> Dict:
        """pylintでチェック（詳細な解析）"""
        try:
            result = subprocess.run(
                [
                    'pylint',
                    '--output-format=json',  # JSON形式で出力
                    filepath
                ],
                capture_output=True,
                text=True
            )
            
            # スコアを取得するために通常形式でも実行
            score_result = subprocess.run(
                ['pylint', '--score=y', filepath],
                capture_output=True,
                text=True
            )
            
            # スコアを抽出
            score = None
            for line in score_result.stdout.split('\n'):
                if 'Your code has been rated at' in line:
                    score_match = re.search(r'([-\d.]+)/10', line)
                    if score_match:
                        score = float(score_match.group(1))
            
            # JSON結果を解析
            issues_by_type = {
                'convention': 0,
                'refactor': 0,
                'warning': 0,
                'error': 0,
                'fatal': 0,
                'info': 0
            }
            
            message_types = {}
            
            try:
                issues = json.loads(result.stdout) if result.stdout else []
                for issue in issues:
                    issue_type = issue.get('type', 'unknown')
                    if issue_type in issues_by_type:
                        issues_by_type[issue_type] += 1
                    
                    # メッセージIDごとにカウント
                    msg_id = issue.get('message-id', 'unknown')
                    message_types[msg_id] = message_types.get(msg_id, 0) + 1
            except json.JSONDecodeError:
                issues = []
            
            return {
                'tool': 'pylint',
                'score': score,
                'issues_by_type': issues_by_type,
                'total_issues': sum(issues_by_type.values()),
                'message_types': dict(sorted(message_types.items(), key=lambda x: x[1], reverse=True)[:10]),  # 上位10件
                'has_errors': issues_by_type.get('error', 0) > 0,
                'has_warnings': issues_by_type.get('warning', 0) > 0
            }
            
        except FileNotFoundError:
            return {
                'tool': 'pylint',
                'error': 'pylint not installed. Please run: pip install pylint'
            }
        except Exception as e:
            return {'tool': 'pylint', 'error': str(e)}
    
    def analyze_code_structure(self, filepath: str) -> Dict:
        """コード構造の分析（型ヒント、docstring、etc）"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            analysis = {
                'total_lines': len(lines),
                'code_lines': 0,
                'comment_lines': 0,
                'docstring_lines': 0,
                'blank_lines': 0,
                'functions': [],
                'classes': [],
                'has_type_hints': False,
                'has_module_docstring': False,
                'imports_count': 0,
                'type_annotations_count': 0
            }
            
            # モジュールレベルのdocstringチェック
            stripped_content = content.strip()
            if stripped_content.startswith('"""') or stripped_content.startswith("'''"):
                analysis['has_module_docstring'] = True
            
            in_docstring = False
            docstring_quotes = None
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                
                # 空行の判定を修正：実際に空白のみの行かチェック
                if not stripped:
                    analysis['blank_lines'] += 1
                    continue
                
                # docstring処理
                if '"""' in stripped or "'''" in stripped:
                    quotes = '"""' if '"""' in stripped else "'''"
                    if not in_docstring:
                        in_docstring = True
                        docstring_quotes = quotes
                        analysis['docstring_lines'] += 1
                    elif quotes == docstring_quotes:
                        in_docstring = False
                        analysis['docstring_lines'] += 1
                    continue
                
                if in_docstring:
                    analysis['docstring_lines'] += 1
                    continue
                
                # コメント行の判定を修正
                if stripped.startswith('#'):
                    analysis['comment_lines'] += 1
                    continue
                
                # ここまで来たらコード行
                analysis['code_lines'] += 1
                
                # import文
                if stripped.startswith('import ') or stripped.startswith('from '):
                    analysis['imports_count'] += 1
                
                # 関数定義（型ヒント付きかチェック）
                if stripped.startswith('def '):
                    func_match = re.match(r'def\s+(\w+)\s*\((.*?)\)', stripped)
                    if func_match:
                        func_name = func_match.group(1)
                        params = func_match.group(2)
                        has_type_hint = '->' in line or ':' in params
                        analysis['functions'].append({
                            'name': func_name,
                            'line': i + 1,
                            'has_type_hints': has_type_hint
                        })
                        if has_type_hint:
                            analysis['has_type_hints'] = True
                            analysis['type_annotations_count'] += 1
                
                # クラス定義
                if stripped.startswith('class '):
                    class_match = re.match(r'class\s+(\w+)', stripped)
                    if class_match:
                        analysis['classes'].append({
                            'name': class_match.group(1),
                            'line': i + 1
                        })
                
                # 変数の型アノテーション
                if re.search(r':\s*(int|str|float|bool|List|Dict|Tuple|Optional|Any|Union)', line):
                    analysis['type_annotations_count'] += 1
                    analysis['has_type_hints'] = True
            
            # 比率計算
            if analysis['total_lines'] > 0:
                analysis['comment_ratio'] = (analysis['comment_lines'] + analysis['docstring_lines']) / analysis['total_lines']
                analysis['code_ratio'] = analysis['code_lines'] / analysis['total_lines']
            else:
                analysis['comment_ratio'] = 0
                analysis['code_ratio'] = 0
            
            return analysis
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_file(self, filepath: str) -> Dict:
        """単一ファイルの完全チェック"""
        full_path = self.code_dir / filepath if not Path(filepath).is_absolute() else Path(filepath)
        
        if not full_path.exists():
            return {'error': f'File not found: {filepath}'}
        
        return {
            'filename': filepath,
            'flake8': self.check_flake8_with_extensions(str(full_path)),
            'pylint': self.check_pylint(str(full_path)),
            'structure': self.analyze_code_structure(str(full_path))
        }
    
    def check_all_files(self, language_patterns: Dict[str, List[str]]) -> Dict:
        """
        言語パターン別にすべてのファイルをチェック
        
        Args:
            language_patterns: {'en': ['file1.py', ...], 'ja': [...], 'mixed': [...]}
        """
        results = {}
        
        for lang, files in language_patterns.items():
            results[lang] = []
            for filepath in files:
                print(f"Checking {lang}/{filepath}...")
                file_result = self.check_file(filepath)
                results[lang].append(file_result)
        
        return results
    
    def generate_comparison_report(self, results: Dict) -> str:
        """詳細な比較レポートの生成"""
        report = []
        report.append("=" * 70)
        report.append("Code Quality Comparison Report")
        report.append("Tools: flake8 (with docstrings & type-checking), pylint")
        report.append("=" * 70)
        
        summary_data = {}
        
        for lang in results:
            report.append(f"\n### Language Pattern: {lang.upper()}")
            report.append("-" * 50)
            
            # 言語別の集計
            lang_summary = {
                'flake8_total': 0,
                'flake8_categories': {},
                'pylint_scores': [],
                'pylint_issues': 0,
                'has_docstrings': 0,
                'has_type_hints': 0,
                'avg_comment_ratio': 0,
                'files_count': len(results[lang])
            }
            
            for file_result in results[lang]:
                # flake8結果の集計
                if 'flake8' in file_result and 'total_issues' in file_result['flake8']:
                    lang_summary['flake8_total'] += file_result['flake8']['total_issues']
                    
                    # カテゴリ別集計
                    for category, count in file_result['flake8'].get('errors_by_category', {}).items():
                        lang_summary['flake8_categories'][category] = \
                            lang_summary['flake8_categories'].get(category, 0) + count
                
                # pylint結果の集計
                if 'pylint' in file_result:
                    pylint_data = file_result['pylint']
                    if 'score' in pylint_data and pylint_data['score'] is not None:
                        lang_summary['pylint_scores'].append(pylint_data['score'])
                    if 'total_issues' in pylint_data:
                        lang_summary['pylint_issues'] += pylint_data['total_issues']
                
                # 構造分析の集計
                if 'structure' in file_result and 'error' not in file_result['structure']:
                    structure = file_result['structure']
                    if structure.get('has_module_docstring'):
                        lang_summary['has_docstrings'] += 1
                    if structure.get('has_type_hints'):
                        lang_summary['has_type_hints'] += 1
                    lang_summary['avg_comment_ratio'] += structure.get('comment_ratio', 0)
            
            # 平均値計算
            if lang_summary['files_count'] > 0:
                lang_summary['avg_comment_ratio'] /= lang_summary['files_count']
                if lang_summary['pylint_scores']:
                    lang_summary['avg_pylint_score'] = sum(lang_summary['pylint_scores']) / len(lang_summary['pylint_scores'])
                else:
                    lang_summary['avg_pylint_score'] = 0
            
            # レポート出力
            report.append(f"\n📊 Summary for {lang.upper()}:")
            report.append(f"  Files analyzed: {lang_summary['files_count']}")
            
            report.append(f"\n  Flake8 Results:")
            report.append(f"    Total issues: {lang_summary['flake8_total']}")
            if lang_summary['flake8_categories']:
                report.append(f"    Issues by category:")
                for category, count in sorted(lang_summary['flake8_categories'].items()):
                    report.append(f"      - {category}: {count}")
            
            report.append(f"\n  Pylint Results:")
            report.append(f"    Average score: {lang_summary['avg_pylint_score']:.2f}/10.0")
            report.append(f"    Total issues: {lang_summary['pylint_issues']}")
            
            report.append(f"\n  Code Quality Metrics:")
            report.append(f"    Files with module docstrings: {lang_summary['has_docstrings']}/{lang_summary['files_count']}")
            report.append(f"    Files with type hints: {lang_summary['has_type_hints']}/{lang_summary['files_count']}")
            report.append(f"    Average comment ratio: {lang_summary['avg_comment_ratio']:.1%}")
            
            summary_data[lang] = lang_summary
        
        # 比較サマリー
        report.append("\n" + "=" * 70)
        report.append("COMPARATIVE ANALYSIS")
        report.append("=" * 70)
        
        if len(summary_data) > 1:
            # 最良のスコアを持つ言語を特定
            best_pylint = max(summary_data.items(), key=lambda x: x[1].get('avg_pylint_score', 0))
            least_issues = min(summary_data.items(), key=lambda x: x[1]['flake8_total'])
            
            report.append(f"\n🏆 Best Practices:")
            report.append(f"  Highest Pylint score: {best_pylint[0]} ({best_pylint[1]['avg_pylint_score']:.2f}/10)")
            report.append(f"  Fewest flake8 issues: {least_issues[0]} ({least_issues[1]['flake8_total']} issues)")
            
            # 詳細な比較
            report.append(f"\n📈 Detailed Comparison:")
            langs = list(summary_data.keys())
            
            # PEP 8準拠度の比較
            report.append(f"\n  PEP 8 Compliance (flake8 issues - lower is better):")
            for lang in langs:
                issues_per_file = summary_data[lang]['flake8_total'] / summary_data[lang]['files_count'] if summary_data[lang]['files_count'] > 0 else 0
                report.append(f"    {lang}: {issues_per_file:.1f} issues/file")
            
            # Docstring使用率の比較
            report.append(f"\n  Documentation Quality:")
            for lang in langs:
                doc_ratio = summary_data[lang]['has_docstrings'] / summary_data[lang]['files_count'] if summary_data[lang]['files_count'] > 0 else 0
                report.append(f"    {lang}: {doc_ratio:.0%} files with module docstrings")
            
            # 型ヒント使用率の比較
            report.append(f"\n  Type Safety:")
            for lang in langs:
                type_ratio = summary_data[lang]['has_type_hints'] / summary_data[lang]['files_count'] if summary_data[lang]['files_count'] > 0 else 0
                report.append(f"    {lang}: {type_ratio:.0%} files with type hints")
        
        report.append("\n" + "=" * 70)
        return "\n".join(report)


# 使用例
if __name__ == "__main__":
    import sys
    
    # コマンドライン引数からディレクトリを取得（デフォルトは"output"）
    code_dir = sys.argv[1] if len(sys.argv) > 1 else "Output"
    
    print(f"Checking code quality in directory: {code_dir}")
    checker = CodeQualityChecker(code_dir)
    
    language_patterns = {
        'en': ['binary_search_tree_en.py'],
        'ja': ['binary_search_tree_Ja.py'],
        'mixed': ['binary_search_tree_mix.py'],
    }
    
    # 単一ファイルのテスト用
    # single_result = checker.check_file('test.py')
    # print(json.dumps(single_result, indent=2, ensure_ascii=False))
    
    # 複数ファイルのチェック実行
    print("\nRunning quality checks...")
    results = checker.check_all_files(language_patterns)
    
    # レポート生成と表示
    report = checker.generate_comparison_report(results)
    print(report)
    
    # 詳細結果をJSON形式で保存
    output_file = 'code_quality_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nDetailed results saved to: {output_file}")