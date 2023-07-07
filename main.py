from Aligner import Aligner
from Reader import Reader
from Verifier import Verifier

def main():
   Read_Object = Reader()
   Verifier_Object = Verifier()

   print("Reading sequences...")
   sequences = Read_Object.get_seqs()
   print("Done!")

   if len(sequences) == 0: 
      print("No sequences found. Terminating...")
      return

   print("Reading Scoring matrix...")
   score = Read_Object.get_scoring()
   print("Done!")

   if score is None:
      print("No scoring matrix found. Terminating...")
      return
   
   Start_Gap_Penalty = float(input("Please input the starting Gap Penalty (Positive number):\n"))
   Cont_Gap_Penalty = float(input("Please input the continued Gap Penalty (Positive number):\n"))

   if Verifier_Object.verify(sequences, score, [Start_Gap_Penalty, Cont_Gap_Penalty]):
      print("All inputs valid")
   else: 
      print("Invalid. Please check inputs. Terminating...")
      return
   
   print("Aligning sequences...")
   Aligner_Object = Aligner(sequences, score, [Start_Gap_Penalty, Cont_Gap_Penalty])
   Aligned_seqs = Aligner_Object .Align_sequences()
   for i in Aligned_seqs:
      print(i)
   return

if __name__ == '__main__':
    main()